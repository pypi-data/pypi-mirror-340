import subprocess
from typing import List, Optional

def uname_info(args: Optional[List[str]] = None) -> str:
    cmd = ['uname']
    if args is not None:
        cmd.extend(args)

    result = subprocess.run(
        args=cmd,
        capture_output=True,
        check=True,
    )

    return result.stdout.decode().strip()