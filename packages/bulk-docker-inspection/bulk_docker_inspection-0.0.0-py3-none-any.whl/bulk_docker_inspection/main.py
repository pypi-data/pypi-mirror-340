import asyncio
import cloudpickle
import os
import subprocess
import shutil
import json
import sys
import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from hashlib import md5
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper, TemporaryDirectory
from typing import Any, Callable, Dict, Iterable, List, Union, Tuple, Set
from warnings import warn

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
RUNNER_PATH = os.path.join(THIS_DIR, 'runner.py')
IMPORTLIB_RUNNER_PATH = os.path.join(THIS_DIR, 'importlib_runner.py')

class LogWriter:
    MODE_ERROR_ONLY = 'error_only'
    MODE_ALWAYS = 'always'

    def __init__(
        self,
        file_path: str,
        tmp_file: NamedTemporaryFile,
        mode = MODE_ERROR_ONLY
    ):
        self.file_path = file_path
        self.mode = mode
        self.tmp_file = tmp_file

    def __enter__(self, ):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        write = False
        if self.mode == self.MODE_ALWAYS:
            write = True
        if self.mode == self.MODE_ERROR_ONLY and exc_type is not None:
            write = True

        if write:
            if self.tmp_file is None:
                warn("Unable to write logs, temporary file is None!")
                return

            self.tmp_file.file.seek(0) # Seems to be needed o/w output is empty
            shutil.copy(self.tmp_file.name, self.file_path)

class _Op(ABC):
    def bring_files(self) -> List[Tuple[Union[str, NamedTemporaryFile], str]]:
        return []

    def bring_commands(self) -> List[str]:
        return []

    @abstractmethod
    def decode(self, files: Dict[str, str]) -> Any:
        pass

    def _load(self) -> str:
        """
        Multi purpose:
        1. Validate `bring_files(...)` / `bring_commands(...)` implementations.
        2. Generate a unique handle for this operation to be referred by.
        """
        if hasattr(self, '_handle'):
            return self._handle

        self.__files: List[Tuple[str, str]] = []
        self.__tmp_files: List[Tuple[NamedTemporaryFile, str]] = []

        op_hash = md5()
        for file, dest_path in self.bring_files():
            if isinstance(file, str):
                assert os.path.isfile(file), "Specified path is not a file: %s" % file
                self.__files.append((file, dest_path))
                path = file 

            elif isinstance(file, _TemporaryFileWrapper):
                self.__tmp_files.append((file, dest_path))
                path = file.name

            else:
                raise ValueError("Object returned from bring_files(...) is not acceptable type: %s -- %s", (type(file), file))

            with open(path, 'rb') as f:
                op_hash.update(f.read())

        self.__commands: List[str] = self.bring_commands()
        for command in self.__commands:
            op_hash.update(command.encode())

        # Save handle as hash
        self._handle = op_hash.hexdigest()

    def _assure_loaded(self):
        if not hasattr(self, '_handle'):
            self._load()

    @property
    def handle(self) -> str:
        self._assure_loaded()
        return self._handle

    @property
    def _files(self) -> Iterable[Tuple[str, str]]:
        """
        Unified way to iterate through the file list.

        Returns:
            Iterable[Tuple[str, str]]: path, dest_path
        """
        self._assure_loaded()
        for file, dest_path in self.__tmp_files:
            file.file.seek(0) # TODO: Is this the right place to put this?
            yield (file.name, dest_path)
        for file, dest_path in self.__files:
            yield(file, dest_path)

    @property
    def _commands(self) -> List[str]:
        self._assure_loaded()
        return self.__commands

    def _copy_files(self, directory: str):
        for file, dest_path in self._files:
            copy_path = os.path.join(directory, dest_path)

            if os.path.exists(copy_path):
                with open(copy_path, 'wb') as f:
                    h1 = md5(f.read())
                with open(file, 'wb') as f:
                    h2 = md5(f.read())

                assert h1 == h2, "File path already exists and contents is different: %s" % copy_path
            else:
                shutil.copy(file, copy_path)

class BringCommands(_Op):
    def __init__(self, commands: List[str]):
        self.commands = commands

    def bring_commands(self) -> List[str]:
        return self.commands

class BringFunc(_Op):
    def __init__(self, func: Callable, interpreter: str = 'python', **kwargs):
        self.func = func
        self.interpreter = interpreter
        self.kwargs = kwargs

        self.dst_path = None

    def bring_files(self) -> List[Tuple[NamedTemporaryFile, str]]:
        tmp_file = NamedTemporaryFile('wt')
        with open(inspect.getabsfile(self.func), 'r') as f:
            tmp_file.file.write(f.read())

        self.dst_path = f"func_{self.func.__qualname__}.py"

        return [(
            tmp_file, self.dst_path
        )]

    def bring_commands(self) -> List[str]:
        try:
            # TODO: Double check the escaping
            serialized_kwargs = f'"{json.dumps(self.kwargs).replace("\"", "\\\"")}"'
        except Exception as err:
            raise RuntimeError("Failed to serialize arguments as json: %s" % self.kwargs)

        return [(
            f"{self.interpreter} importlib_runner.py {self.dst_path} {self.func.__name__} {serialized_kwargs}"
        )]

    def decode(self, files: Dict[str, str]) -> Any:
        with open(files['out.json'], 'r') as f:
            return json.load(f)['result'] # Little hacky to get most kinds of serialization working


class BringCloudPickle(_Op):
    def __init__(self, func: Callable, interpreter: str = 'python', **kwargs):
        self.func = func
        self.interpreter = interpreter
        self.kwargs = kwargs

        self.dst_path = None

    def bring_files(self) -> List[Tuple[NamedTemporaryFile, str]]:
        self.dst_path = f"func_{self.func.__qualname__}.cpkl"

        pickle = NamedTemporaryFile()
        with open(pickle.name, 'wb') as f:
            cloudpickle.dump(self.func, f)

        return [(
            pickle, self.dst_path
        )]

    def bring_commands(self) -> List[str]:
        try:
            serialized = json.dumps(self.kwargs)
        except Exception as err:
            raise RuntimeError("Failed to serialize arguments as json: %s" % self.kwargs)

        return [
            f"{self.interpreter} runner.py {self.dst_path} {serialized}"
        ]

@dataclass
class RunResult:
    data: dict

    def func_results(self, handle: str) -> Iterable[Tuple[str, Any]]:
        """
        Returns the results of a function execution across all images,

        Example:
        ```
        inspection = bdi.BDI()
        py_version = inspection.add_func(
            bdi.samples.python_version,
            interpreter='python3'
        )

        results = inspection.inspect([
            "ros:iron",
            "ros:humble",
            "ros:galactic"
        ])

        for image, result in results.func_results(py_version):
            print(f"{image}: {result}")
        >>> ros:humble: /usr/bin/python3: 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0]
        >>> ros:galactic: /usr/bin/python3: 3.8.10 (default, Nov 22 2023, 10:22:35) [GCC 9.4.0]
        >>> ros:iron: /usr/bin/python3: 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0]
        ```

        Returns:
            Iterable[str, Any]: image, and returned data.
        """
        for image, results in self.data.items():
            yield image, results[handle]

class BDI:
    def __init__(self):
        self._ops: List[_Op] = []

        self._comm = asyncio.Queue()
        self._log_dir = 'bdi_logs'

        os.makedirs(self._log_dir, exist_ok=True)

    def add_func(
        self,
        func: Callable,
        interpreter: str = 'python',
        **kwargs
    ) -> str:
        op = BringFunc(func=func, interpreter=interpreter, **kwargs)
        self._ops.append(
            op
        )
        return op.handle

    def add_commands(self, commands: str):
        self._ops.append(
            BringCommands(commands)
        )

    def inspect(
        self,
        images: Union[str, List[str]],
        write_logs: bool = True
    ) -> RunResult:
        self._verify_docker()
        if isinstance(images, str):
            images = set((images,))
        else: 
            images = set(images)

        return RunResult(
            asyncio.run(self._inspect(images, write_logs=write_logs))
        )

    async def _inspect(self, images: Union[str, Set[str]], write_logs: bool):
        mount_dir = self.create_mount()

        print_handler = asyncio.create_task(self._handle_prints())
        inspections = []
        for image in images:
            inspections.append(self._inspect_image(
                image=image,
                mount_dir=mount_dir,
                write_logs=write_logs
            ))

        # Wait for inspections to finish
        combined_data = {}
        for result in asyncio.as_completed(inspections):
            image, data = await result

            combined_data[image] = data

        # Shutdown print handler
        await self._comm.put(None)
        await print_handler

        return combined_data

    def create_mount(self, debug: bool = True) -> TemporaryDirectory:
        mount_dir = TemporaryDirectory(prefix="bdi_", delete=False)

        shutil.copy(
            RUNNER_PATH,
            os.path.join(mount_dir.name, 'runner.py')
        )
        shutil.copy(
            IMPORTLIB_RUNNER_PATH,
            os.path.join(mount_dir.name, 'importlib_runner.py')
        )

        script_path = os.path.join(mount_dir.name, "script.sh")
        with open(script_path, 'w') as script:
            script.write("set -e\n")
            for op in self._ops:
                op._copy_files(mount_dir.name)

                if len(op._commands) != 0:
                    script.write("# ------\n")
                    out_dir = os.path.join("/bdi_out", op.handle)
                    script.write(f"mkdir -p {out_dir}\n")
                    script.write(f"export OUT_DIR={out_dir}\n")
                    for command in op._commands:
                        script.write(command + "\n")

        if debug:
            print("Mount directory contents:")
            for file in os.listdir(mount_dir.name):
                print(f"- {file}")

            print("Script contents")
            with open(script_path, 'r') as f:
                print("\n".join([f"  {line}" for line in f.read().split("\n")]))

        return mount_dir

    async def _inspect_image(
        self,
        image: str,
        mount_dir: TemporaryDirectory,
        write_logs: bool
    ) -> dict:
        tmp_file = NamedTemporaryFile('wt')
        log_writer = LogWriter(
            file_path=os.path.join(self._log_dir, f"{image}.txt"),
            tmp_file=tmp_file,
            mode=LogWriter.MODE_ERROR_ONLY if not write_logs else LogWriter.MODE_ALWAYS
        )
        with log_writer:
            await self._comm.put("[▼] Pulling image: %s" % image)

            proc = await asyncio.create_subprocess_exec(
                *['docker', 'pull', image],
                stderr=tmp_file.file,
                stdout=tmp_file.file
            )
            await proc.wait()

            if proc.returncode != 0:
                raise RuntimeError("Docker pull failed (code: %s), please see associated log file in bdi_logs/" % proc.returncode)

            await self._comm.put("[►] Running docker container: %s" % image)
            output_dir = TemporaryDirectory()
            run_command = [
                'docker', 'run', '--rm', # '-it',
                '--attach', 'stdout', '--attach', 'stderr',
                '-v', f'{mount_dir.name}:/bdi:ro', # RO is important!
                '-v', f'{output_dir.name}:/bdi_out:rw',
                image
            ]
            run_command.extend(
                # `sh -c` b/c `exec` is not a shell environ (https://unix.stackexchange.com/a/669921/388962)
                ['sh', '-c', "cd /bdi && bash /bdi/script.sh"] # '.split(' ')
            )

            # NOTE: If `flush` is not set, these prints may end up AFTER the subsequent logs.
            print("\n# DOCKER COMMAND:", file=tmp_file.file, flush=True)
            print(f"# {' '.join(run_command)}\n", file=tmp_file.file, flush=True)

            proc = await asyncio.create_subprocess_exec(
                *run_command,
                stderr=tmp_file.file,
                stdout=tmp_file.file
            )
            await proc.wait()

            if proc.returncode != 0:
                raise RuntimeError("Docker run failed (code: %s), please see associated log file in bdi_logs/" % proc.returncode)

            # Decode each operation
            data = {}
            for op in self._ops:
                op_output_dir = os.path.join(output_dir.name, op.handle)

                # Send file list and path on host machine to decode func
                file_map = {}
                for file in os.listdir(op_output_dir):
                    file_map[file] = os.path.join(op_output_dir, file)

                data[op.handle] = op.decode(file_map)

            await self._comm.put(f"[✔] Docker process completed successfully: {image}")
            return image, data 

    async def _handle_prints(self):
        while True:
            statement = await self._comm.get()
            if statement is None:
                return

            print(statement, flush=True)

    def _verify_docker(self):
        assert is_cmd("docker"), "Docker command not found, script is unable to run."
        print("Found docker!")

        # Issue docker info command to assure the docker server (daemon) is running
        result = subprocess.run(
            args=['docker', 'info'],
            stderr=sys.stderr,
            stdout=sys.stdout
        )

        if result.returncode != 0:
            raise RuntimeError("Unable to verify docker CLI is functional, please see output above for errors.")

def is_cmd(cmd: str) -> bool:
    """
    Utility for assuring that a command is valid through use of `which`.

    Returns:
        bool: Indicating if the command was found.
    """

    args = ['which', cmd]
    result = subprocess.run(
        args=args
    )

    if result.returncode == 0:
        return True
    elif result.returncode == 1:
        return False
    else:
        warn("Unexpected return code '%s' from command: %s" % (result.returncode, ' '.join(args)))
        return False