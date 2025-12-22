'''
PY DBMS — DB client CLI
Copyright (C) 2025  Anish Sethi
Licensed under - BSD-3-Clause License
Version - 2.1
Release - Stable
'''

from .Global import Print, console, config
from .dependencies import pyfiglet, Text, Table, Align, Rule, Panel, mysql, sys
from .pydbms_mysql import execute, execute_change, execute_select, connect, get_query_mysql
from .config import parse_query_config, coerce_value_config, save_config, get_default_value_config, validate_config_types

def print_banner() -> None:
    ascii_art = pyfiglet.figlet_format("PY   DBMS", font="slant").rstrip()
    
    logo = Text(ascii_art, style="bold color(57)") 
    
    stats_table = Table(show_header=False, box=None, expand=True)
    stats_table.add_column("1", justify="center", ratio=1)
    stats_table.add_column("2", justify="center", ratio=1)
    stats_table.add_column("3", justify="center", ratio=1)

    stats_table.add_row(
        "[bold cyan]v2.1[/]\n [bold white]Version[/]",
        "[bold yellow]MySQL[/]\n[bold white]Currently Supported[/]", 
        "[bold green]Online since 2025[/]\n[bold white]Status[/]"
    )
    
    author = Text("Anish Sethi  •  Delhi Technological University", style="bright_white")

    License = Text("Licensed Under BSD-3-Clause License (see .version for more info)", style="dim white")

    content = [
        Align(logo, align="center"),
        Text("\n"), 
        Rule(style="dim purple"), 
        Text("\n"), 
        stats_table,
        Text("\n"), 
        Align(author, align="center"),
        Align(License, align="center"),
    ]

    from rich.console import Group
    panel_content = Group(*content)

    console.print(
        Panel(
            panel_content,
            border_style="color(57)", 
            title="[bold white] SECURE TERMINAL [/]",
            title_align="center",
            padding=(1, 2),
            expand=True 
        )
    )
    print('\n\n')
    
def build_section_table(section: dict) -> Table:
    table = Table(show_header=False, box=None)
    table.add_column("", style="white", no_wrap=True)
    table.add_column("", style="dim white")
    for key, value in section.items():
        table.add_row(key, str(value))

    return table
        
def meta(cmd: str, cur: object) -> None:
    cmd = cmd.strip()

    # .help
    if cmd == ".help":
        help_table = Table(title="Helper Commands", show_header=False, header_style="bold cyan")
        help_table.add_column("Command", no_wrap=True)
        help_table.add_column("Description", style="white", no_wrap=True)
        help_table.add_row(".help", "Show helper commands")
        help_table.add_row(".databases", "Show databases in current connection")
        help_table.add_row(".tables", "Show tables in current database")
        help_table.add_row(".schema <table>", "Show CREATE TABLE statement for table <table>")
        help_table.add_row(".clear", "Clear the terminal screen")
        help_table.add_row(".version", "Show pydbms build information")
        help_table.add_row(".config", "Show config settings for pydbms")
        help_table.add_row(".config set <section>.<key> <value>", "Set config to a new value")
        help_table.add_row(".config reset <section>.<key>", "Reset config to a default value")
        help_table.add_row(".exit", "Exit pydbms")
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
        info.add_column("", style="white", no_wrap=True)
        info.add_column("", style="dim white")

        info.add_row("Name", "[link=https://github.com/Anish-Sethi-12122/py-dbms-cli]pydbms Terminal[/link]")
        info.add_row("Version", "v2.1")
        info.add_row("Build", "Stable Release")
        info.add_row("Python", f"[link=https://www.python.org/]{sys.version.split()[0]}[/link]")
        info.add_row("Author", "[link=https://www.linkedin.com/in/anish-sethi-dtu-cse/]Anish Sethi[/link]")
        info.add_row("Institution", "B.Tech Computer Science and Engineering @ Delhi Technological University")
        info.add_row("Licensed under", "[link=https://opensource.org/license/bsd-3-clause]BSD-3-Clause License[/link]")

        console.print(
            Panel(
                info,
                title="[bold white]PYSQL Terminal — Build Info[/]",
                border_style="bright_magenta",
                padding=(1, 2),
            )
        )
        console.print()
        console.print("Run `pip install -U py-dbms-cli` in terminal to check for updates.",style="dim white")
        console.print()
        return
        
    # .config
    if cmd == ".config":
        outer = Table(show_header=False, box=None)
        outer.add_column("", style="bold white", no_wrap=True)
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
                title="[bold white]PYSQL Terminal — config settings[/]",
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
            Print("Usage: .config set <section>.<key> <value>", "YELLOW")
            return

        _, _, path, raw_value = parts
        
        parsed = parse_query_config(path)
        
        if not parsed:
            Print("Invalid input format. Use <section>.<key>", "RED")
            return

        section, key = parsed
        
        if section not in config or key not in config[section]:
            Print(f"Unknown config key: {path}", "RED")
            return

        value = coerce_value_config(raw_value)
        config[section][key] = value
        save_config(config)

        Print(f"Updated {path} → {value}", "GREEN")
        return

    # .config reset or .config -d or .config --default
    if cmd.startswith(".config reset"):
        parts = cmd.split(maxsplit=2)

        if len(parts) != 3:
            Print("Usage: .config reset <section>.<key>", "YELLOW")
            return

        path = parts[2]
        parsed = parse_query_config(path)

        if not parsed:
            Print("Invalid config key format. Use <section>.<key>", "RED")
            return

        section, key = parsed
        default = get_default_value_config(section, key)

        if default is None:
            Print(f"No default value for {path}.", "RED")
            return

        config[section][key] = default
        save_config(config)

        Print(f"Reset {path} → {default}", "GREEN")
        return

    # .exit
    if cmd == ".exit":
        Print("Session Terminated.", "RED", "bold")
        sys.exit()

    Print(f"Unknown command: {cmd}\nRefer to `.help` for list of commands", "YELLOW")

def main():
    global config
    config = validate_config_types()
    if config["ui"].get("show_banner", True):
        print_banner()
        
    con, cur = connect()
    
    Print("Welcome to PY DBMS. If you are unsure where to start, here are some helper commands.", "YELLOW")
    print("\n\n")
    meta(".help",cur)
    
    while True:
        query=get_query_mysql()
            
        if query.strip().startswith("."):
            meta(query.strip(), cur)
            continue
        
        if query.lower().strip()=="exit;":
            Print("Session Terminated.", "RED", "bold")
            sys.exit()
            
        q = query.lower().strip()
        if q.startswith(("select","with","desc","describe","show")):
            try:
                execute_select(query, cur)
            except mysql.Error as err:
                console.print(f"{err.msg}", style="bold red")
                
        elif q.startswith(("update","delete","insert","drop")):
            try:
                execute_change(query,con,cur)
            except mysql.Error as err:
                console.print(f"{err.msg}",style="bold red")
                
        else:
            try:
                execute(query,cur)
            except mysql.Error as err:
                console.print(f"{err.msg}",style="bold red")

if __name__=="__main__":
    main()
