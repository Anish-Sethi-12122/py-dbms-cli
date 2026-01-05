# pydbms/pydbms/Global.py

from .dependencies import Console, time, datetime, pwinput, sys, mysql
from .config import load_config

console=Console()
config = load_config()

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
        
def current_datetime() -> str:
    current_datetime = datetime.datetime.now()

    Year = current_datetime.year
    Month = current_datetime.month
    Day = current_datetime.day
    Hour = current_datetime.hour
    Minute = current_datetime.minute
    Second = current_datetime.second
    
    return f"{Year}-{Month}-{Day}_{Hour}-{Minute}-{Second}"
