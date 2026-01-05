from .dependencies import sys, os

def pydbms_dir() -> str:
    if sys.platform.startswith("win"):
        base = os.getenv("APPDATA")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.local/share")

    path = os.path.join(base, "pydbms")
    os.makedirs(path, exist_ok=True)
    return path

def pydbms_path(*parts) -> str:
    return os.path.join(pydbms_dir(), *parts)
