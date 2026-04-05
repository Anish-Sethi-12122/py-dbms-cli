# pydbms/pydbms/main/runtime.py

import time
from datetime import datetime
from .dependencies import pydbms_version
import copy
from .config import load_config, DEFAULT_CONFIG
from rich.console import Console

console=Console()
ver = pydbms_version(distribution_name="py-dbms-cli")

def Print(message: str, color_key: str ="WHITE", style: str = "", slow_type: bool = True) -> None:
    COLOR_MAP = {
        "CYAN": "bright_cyan",
        "YELLOW": "bright_yellow",
        "RED": "bright_red",
        "GREEN": "bright_green",
        "WHITE": "white",
        "MAGENTA": "bright_magenta"
    }
    color = COLOR_MAP.get(color_key, "white")
    delay = 0.02069 if slow_type else 0
    for char in message:
        if char == "\n":
            console.print()
            continue
        console.print(char, style=f"{style} {color}", end="")
        time.sleep(delay)

def PrintNewline(count: int = 1) -> None:
    """Print blank lines. Replaces bare console.print() spacing calls."""
    for _ in range(count):
        console.print()
        
def current_datetime() -> str:
    """Return a timestamp string suitable for filenames."""
    now = datetime.now()

    Year = now.year
    Month = now.month
    Day = now.day
    Hour = now.hour
    Minute = now.minute
    Second = now.second
    
    return f"{Year}-{Month}-{Day}_{Hour}-{Minute}-{Second}"

def load_config_safe() -> dict:
    try:
        return load_config()
    except Exception as e:
        Print(f"\npydbms error> Error loading config: {e}\n", "RED")
        return copy.deepcopy(DEFAULT_CONFIG)

config = load_config_safe()