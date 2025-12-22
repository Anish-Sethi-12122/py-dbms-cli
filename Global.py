#Global functions and variables used across all/major files

from .dependencies import Console, time, sys, os
from .config import load_config

console=Console()
config = load_config()

def Print(message: str, color_key="WHITE", style="", type=True) -> None:
    COLOR_MAP = {
        "CYAN": "bright_cyan",
        "YELLOW": "bright_yellow",
        "RED": "bright_red",
        "GREEN": "bright_green",
        "WHITE": "white",
        "MAGENTA": "bright_magenta"
    }
    color = COLOR_MAP.get(color_key, "white")
    delay = 0.02069 if type else 0
    for char in message:
        if char == "\n":
            console.print()
            continue
        console.print(char, style=f"{style} {color}", end="")
        time.sleep(delay)
        
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