'''
PY DBMS — DB client CLI
Copyright (C) 2025  Anish Sethi
Licensed under - BSD-3-Clause License
Version - 2.5.0
Release - Stable
'''

from .Global import Print, console, config
from .dependencies import pyfiglet, Text, Table, Align, Rule, Panel, mysql, sys, Group
from .pydbms_mysql import execute, execute_change, execute_select, connect, get_query_mysql
from .config import parse_query_config, coerce_value_config, save_config, get_default_value_config, validate_config_types, DEFAULT_SESSION_CONFIG, SESSION_CONFIG

QUERY_HANDLERS = {
    "select": execute_select,
    "change": execute_change,
    "ddl": execute_change,
    "other": execute,
}

def print_banner() -> None:
    ascii_art = pyfiglet.figlet_format("PY   DBMS", font="slant").rstrip()
    
    logo = Text(ascii_art, style="bold color(57)") 
    
    banner_table = Table(show_header=False, box=None, expand=True)
    banner_table.add_column("1", justify="center", ratio=1)
    banner_table.add_column("2", justify="center", ratio=1)
    banner_table.add_column("3", justify="center", ratio=1)
    banner_table.add_column("4", justify="center", ratio=1)

    banner_table.add_row(
        "[bold cyan]v2.5.0[/]\n [bold white]Version[/]",
        "[bold yellow]MySQL[/]\n[bold white]Currently Supported[/]", 
        "[bold green]Online since 2025[/]\n[bold white]Status[/]",
        "[bold magenta]Stable[/]\n[bold white]Release[/]"
    )
    
    author = Text("Anish Sethi  •  Delhi Technological University  •  Class of 2029", style="bright_white")

    License = Text("Licensed Under BSD-3-Clause License (see .version for more info)", style="dim white")

    content = [
        Align(logo, align="center"),
        Text("\n"), 
        Rule(style="dim purple"), 
        Text("\n"), 
        banner_table,
        Text("\n"), 
        Align(author, align="center"),
        Align(License, align="center"),
    ]

    panel_content = Group(*content)

    console.print(
        Panel(
            panel_content,
            border_style="color(57)", 
            title="[bold white] PYDBMS TERMINAL [/]",
            title_align="center",
            padding=(1, 2),
            expand=True 
        )
    )
    print('\n\n')
    
def build_section_table(section: dict) -> Table:
    table = Table(show_header=False, box=None)
    table.add_column("", style="white", overflow="ellipsis")
    table.add_column("", style="dim white")
    for key, value in section.items():
        table.add_row(key, str(value))

    return table
        
def meta(cmd: str, cur: object, con=None) -> None:
    cmd = cmd.strip()

    # .help
    if cmd == ".help":
        help_table = Table(title="Helper Commands", show_header=False, border_style="bold magenta")
        help_table.add_column("Command", overflow="ellipsis")
        help_table.add_column("Description", style="white", overflow="ellipsis")
        help_table.add_row(".help", "Show helper commands")
        help_table.add_row(".databases", "Show databases in current connection")
        help_table.add_row(".tables", "Show tables in current database")
        help_table.add_row(".schema <table>", "Show CREATE TABLE statement for table <table>")
        help_table.add_row(".clear", "Clear the terminal screen")
        help_table.add_row(".version", "Show pydbms build information")
        help_table.add_row(".config", "Show config settings for pydbms")
        help_table.add_row(".config set <section>.<key> <value>", "Set config to a new value")
        help_table.add_row(".config reset <section>.<key>", "Reset config to a default value")
        help_table.add_row(".session-config", "Show session config settings for pydbms (Resets on every run)")
        help_table.add_row(".session-config set <key> <value>", "Set session config to a new value")
        help_table.add_row(".session-config reset <key>", "Reset session config to a default value")
        help_table.add_row(".exit", "Exit pydbms")
        console.print(help_table)
        console.print()
        
        console.print()
        help_table = Table(title="Helper Flags", show_header=False, border_style="bold magenta")
        help_table.add_column("Flag Usage", overflow="ellipsis")
        help_table.add_column("Description", style="white", overflow="ellipsis")
        help_table.add_row("--expand", "Show full cell value without wrap")
        console.print(help_table)
        console.print()
        return

    # .databases
    if cmd == ".databases":
        try:
            execute_select("SHOW DATABASES;",cur)
        except mysql.Error as err:
            Print(err.msg, "RED", "bold")
        return
            
    # .tables
    if cmd == ".tables":
        try:
            execute_select("SHOW TABLES;",cur)
        except mysql.Error as err:
            Print(err.msg, "RED", "bold")
        return

    # .schema table_name
    if cmd.startswith(".schema"):
        parts = cmd.split()
        if len(parts) != 2:
            print("Usage: .schema <table_name>\n")
            return
        table = parts[1]
        try:
            cur.execute(f"SHOW CREATE TABLE {table};")
            row = cur.fetchone()
            if row:
                print(row[1])
                print()
            else:
                print(f"No such table: {table}\n")
        except mysql.Error as err:
            print(err.msg)
        return

    # .clear
    if cmd == ".clear":
        import os
        os.system("cls" if os.name == "nt" else "clear")
        print()
        return
    
    # .version
    if cmd == ".version":
        console.print()
        info = Table(show_header=False, box=None)
        info.add_column("", style="white", overflow="ellipsis")
        info.add_column("", style="dim white")

        info.add_row("Name", "[link=https://github.com/Anish-Sethi-12122/py-dbms-cli]pydbms Terminal[/link]")
        info.add_row("Version", "v2.5.0")
        info.add_row("Build", "Stable Release")
        info.add_row("Python", f"[link=https://www.python.org/]{sys.version.split()[0]}[/link]")
        info.add_row("MySQL", f"[link=https://www.mysql.com/]{con.get_server_info()}[/link]")
        info.add_row("Author", "[link=https://www.linkedin.com/in/anish-sethi-dtu-cse/]Anish Sethi[/link]")
        info.add_row("Institution", "B.Tech Computer Science and Engineering @ Delhi Technological University")
        info.add_row("Licensed under", "[link=https://opensource.org/license/bsd-3-clause]BSD-3-Clause License[/link]")

        console.print(
            Panel(
                info,
                title="[bold white]PYDBMS Terminal — Build Info[/]",
                border_style="bright_magenta",
                padding=(1, 2),
            )
        )
        console.print()
        console.print("Run `pip install -U py-dbms-cli` in terminal to check for updates.\n\n",style="dim white")
        console.print("NOTE: Run `pip install --upgrade py-dbms-cli` in terminal directly to install the latest version.\n",style="dim white")
        console.print()
        return
        
    # .config
    if cmd == ".config":
        outer = Table(show_header=False, box=None)
        outer.add_column("", style="bold white", overflow="ellipsis")
        outer.add_column("", style="white")

        # UI section
        ui_cfg = config.get("ui", {})
        outer.add_row("UI", build_section_table(ui_cfg))
        
        outer.add_row("", "")

        # MySQL section
        mysql_cfg = config.get("mysql", {})
        outer.add_row("MySQL",build_section_table(mysql_cfg))

        console.print(
            Panel(
                outer,
                title="[bold white]PYDBMS Terminal — config settings[/]",
                border_style="bright_magenta",
                padding=(1, 2),
            )
        )

        console.print()
        return
    
    # .config set
    if cmd.startswith(".config set"):
        parts = cmd.split(maxsplit=3)

        if len(parts) != 4:
            Print("Invalid input format.\n", "RED")
            Print("Usage: .config set <section>.<key> <value>", "YELLOW")
            console.print()
            return

        _, _, path, raw_value = parts
        
        parsed = parse_query_config(path)
        
        if not parsed:
            Print("Invalid input format. Use <section>.<key>", "RED")
            console.print()
            return

        section, key = parsed
        section=section.lower()
        key=key.lower()
        
        if section not in config or key not in config[section]:
            Print(f"Unknown config key: {path}", "RED")
            console.print()
            return

        value = coerce_value_config(raw_value)
        config[section][key] = value
        save_config(config)

        Print(f"Updated {path} → {value}", "GREEN")
        console.print()
        return

    # .config reset
    if cmd.startswith(".config reset"):
        parts = cmd.split(maxsplit=2)

        if len(parts) != 3:
            Print("Invalid config key format.\n", "RED")
            Print("Usage: .config reset <section>.<key>", "YELLOW")
            console.print()
            return

        path = parts[2]
        parsed = parse_query_config(path)

        if not parsed:
            Print("Invalid config key format. Use <section>.<key>", "RED")
            console.print()
            return

        section, key = parsed
        section=section.lower()
        key=key.lower()
        default = get_default_value_config(section, key)

        if default is None:
            Print(f"No default value for {path}.", "RED")
            console.print()
            return

        config[section][key] = default
        save_config(config)

        Print(f"Reset {path} → {default}", "GREEN")
        console.print()
        return
    
    # .session-config
    if cmd == ".session-config":
        outer = Table(show_header=False, box=None)
        outer.add_column("", style="white", overflow="ellipsis")

        outer.add_row(build_section_table(SESSION_CONFIG))

        console.print(
            Panel(
                outer,
                title="[bold white]PYDBMS Terminal — Configuration Settings for Current Session[/]",
                border_style="bright_magenta",
                padding=(1, 2),
            )
        )

        console.print()
        return
    
    # .session-config set
    if cmd.startswith(".session-config set"):
        parts = cmd.split(maxsplit=3)

        if len(parts) != 4:
            Print("Invalid input format.\n", "RED")
            Print("Usage: .session-config set <key> <value>\n", "YELLOW")
            console.print()
            return

        _, _, key, raw_value = parts
        key = key.lower()

        if key not in SESSION_CONFIG:
            Print(f"Unknown session config key: {key}", "RED")
            console.print()
            return

        value = coerce_value_config(raw_value)
        SESSION_CONFIG[key] = value

        Print(f"Updated session-config {key} → {value}", "GREEN")
        console.print()
        return

    # .session-config reset
    if cmd.startswith(".session-config reset"):
        parts = cmd.split(maxsplit=2)

        if len(parts) != 3:
            Print("Invalid input format.\n", "RED")
            Print("Usage: .session-config reset <key>\n", "YELLOW")
            console.print()
            return

        key = parts[2].lower()

        if key not in DEFAULT_SESSION_CONFIG:
            Print(f"Unknown session config key: {key}", "RED")
            console.print()
            return

        SESSION_CONFIG[key] = DEFAULT_SESSION_CONFIG[key]

        Print(f"Reset session-config {key} → {DEFAULT_SESSION_CONFIG[key]}", "GREEN")
        console.print()
        return

    # .exit
    if cmd == ".exit":
        Print("Session Terminated.", "RED", "bold")
        console.print()
        sys.exit()

    Print(f"Unknown command: {cmd}\nRefer to `.help` for list of commands", "YELLOW")
    console.print()

def classify_query(query: str) -> str:
    q = query.strip().lower()

    if q.startswith("."):
        return "meta"

    if q.startswith(("select", "with", "show", "desc", "describe", "explain")):
        return "select"

    if q.startswith(("insert", "update", "delete")):
        return "change"

    if q.startswith(("create", "drop", "alter", "truncate")):
        return "ddl"

    return "other"

def main():
    global config
    config = validate_config_types()
    if config["ui"].get("show_banner", True):
        print_banner()
        
    con, cur = connect()
    
    Print("Welcome to PY DBMS. If you are unsure where to start, here are some helper commands.", "YELLOW")
    console.print()
    console.print()
    meta(".help",cur)
    
    while True:
        query = get_query_mysql()

        if query.lower().strip() == "exit;":
            Print("Session Terminated.", "RED", "bold")
            sys.exit()

        query_type = classify_query(query)

        if query_type == "meta":
            meta(query.strip(), cur, con)
            continue

        query_handle = QUERY_HANDLERS.get(query_type, execute)

        try:
            if query_handle is execute_change:
                query_handle(query, con, cur)
            else:
                query_handle(query, cur)
                
        except mysql.Error as err:
            console.print(f"{err.msg}", style="bold red")

if __name__=="__main__":
    main()
