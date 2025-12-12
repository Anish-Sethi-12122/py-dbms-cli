#Global functions and variables used across all/major files

from .dependencies import Console, time

console=Console()

def Print(message, color_key="WHITE", style="", type=True):
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