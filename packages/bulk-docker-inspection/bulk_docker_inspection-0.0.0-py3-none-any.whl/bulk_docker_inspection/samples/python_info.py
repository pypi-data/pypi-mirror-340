import sys

def python_version():
    return f"{sys.executable}: {sys.version}"

def pip_freeze():
    raise NotImplementedError()