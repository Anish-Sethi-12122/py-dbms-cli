# pydbms/pydbms/main/meta_handler.py

from .dependencies import Table, Panel, sys, mysql, copy
from .runtime import Print, config, console, ver
from .pydbms_mysql import execute_select
from .config import parse_query_config, save_config, get_default_value_config, DEFAULT_SESSION_CONFIG, SESSION_CONFIG, DEFAULT_CONFIG

def confirm_reset(prompt: str) -> bool:
    while True:
        Print(prompt, "YELLOW", slow_type=False)
        Print("\n\nYour Input: ", "YELLOW", slow_type=False)
        choice = input().strip().lower()

        if choice in ("yes", "y"):
            return True
        if choice in ("no", "n"):
            return False

        Print("Please type yes or no.\n", "RED", slow_type=False)

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
        help_table.add_column("Description", style="white", no_wrap=True)
        help_table.add_row(".help", "Show helper commands")
        help_table.add_row(".databases", "Show databases in current connection")
        help_table.add_row(".tables", "Show tables in current database")
        help_table.add_row(".schema <table>", "Show CREATE TABLE statement for table <table>")
        help_table.add_row(".clear", "Clear the terminal screen")
        help_table.add_row(".version", "Show pydbms build information")
        help_table.add_row(".config", "Show config settings for pydbms")
        help_table.add_row(".config set <section>.<key> <value>", "Set config to a new value")
        help_table.add_row(".config reset <section?>.<key?>", "Reset config to a default value")
        help_table.add_row(".session-config", "Show session config settings for pydbms (Resets on every run)")
        help_table.add_row(".session-config set <key> <value>", "Set session config to a new value")
        help_table.add_row(".session-config reset <key?>", "Reset session config to a default value")
        help_table.add_row(".exit", "Exit pydbms")
        console.print(help_table)
        console.print()
        
        console.print()
        help_table = Table(title="Helper Flags", show_header=False, border_style="bold magenta")
        help_table.add_column("Flag Usage", overflow="ellipsis")
        help_table.add_column("Description", style="white", no_wrap=True)
        help_table.add_row("--expand", "Show full cell value without wrap (overrides session-config)")
        help_table.add_row("--export <format> <path?>", "Export a query result. Supports -> csv, json")
        console.print(help_table)
        console.print()
        return

    # .databases
    if cmd == ".databases":
        try:
            execute_select("SHOW DATABASES;",cur)
        except mysql.Error as err:
            Print(err.msg, "RED", "bold")
            console.print()
        return
            
    # .tables
    if cmd == ".tables":
        try:
            execute_select("SHOW TABLES;",cur)
        except mysql.Error as err:
            Print(err.msg, "RED", "bold")
            console.print()
        return

    # .schema table_name
    if cmd.startswith(".schema"):
        parts = cmd.split()
        if len(parts) != 2:
            print("Usage: .schema <table_name>\n")
            console.print()
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
            console.print()
        return

    # .clear
    if cmd == ".clear":
        import os
        os.system("cls" if os.name == "nt" else "clear")
        console.print()
        return
    
    # .version
    if cmd == ".version":
        console.print()
        info = Table(show_header=False, box=None)
        info.add_column("", style="white", overflow="ellipsis")
        info.add_column("", style="dim white")

        info.add_row("Name", "[link=https://github.com/Anish-Sethi-12122/py-dbms-cli]pydbms Terminal[/link]")
        info.add_row("Version", f"{ver}")
        info.add_row("Build", "Stable Release")
        info.add_row("Python", f"[link=https://www.python.org/]{sys.version.split()[0]}[/link]")
        mysql_info = con.get_server_info() if con else "Not Connected"
        info.add_row("MySQL", f"[link=https://www.mysql.com/]{mysql_info}[/link]")
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
        mysql_cfg = config.get("mysql", {}).copy()
        try:
            cur.execute("SELECT DATABASE();")
            row = cur.fetchone()
            mysql_cfg["database"] = row[0] if row else None
        except Exception:
            mysql_cfg["database"] = None

        outer.add_row("MySQL", build_section_table(mysql_cfg))

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
        section = section.lower()
        key = key.lower()

        if section not in config or key not in config[section]:
            Print(f"Unknown config key: {path}", "RED")
            console.print()
            return

        current_value = config[section][key]
        expected_type = type(current_value)

        try:
            if expected_type is bool:
                val = raw_value.lower()
                if val in ("true", "1", "yes", "on"):
                    value = True
                elif val in ("false", "0", "no", "off"):
                    value = False
                else:
                    raise ValueError("Invalid boolean")
            else:
                value = expected_type(raw_value)

        except Exception:
            Print(
                f"Invalid value for {path}. Expected {expected_type.__name__}.",
                "RED"
            )
            console.print()
            return

        config[section][key] = value
        save_config(config)

        Print(f"Updated {path} → {value}", "GREEN")
        console.print()
        return
    
    #.config reset
    if cmd == ".config reset":
        Print("pydbms warning: This command will reset all fields in config to default values.\n", "YELLOW")
        
        confirm = confirm_reset("Confirm reset (yes/no): ")

        if not confirm:
            Print("Config reset aborted.\n", "GREEN")
            console.print()
            return

        config.clear()
        config.update(copy.deepcopy(DEFAULT_CONFIG))
        save_config(config)

        Print("All config values reset to default.", "GREEN")
        console.print()
        return
    
    # .config reset <key?>
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
        section = section.lower()
        key = key.lower()

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

        current_value = SESSION_CONFIG[key]
        expected_type = type(current_value)

        if expected_type is bool:
            if raw_value.lower() in ("true", "1", "yes", "on"):
                value = True
            elif raw_value.lower() in ("false", "0", "no", "off"):
                value = False
            else:
                Print(f"Invalid value for {path}. Expected boolean (true/false).\n","RED")
                console.print()
                return
        else:
            try:
                value = expected_type(raw_value)
            except Exception:
                Print(f"Invalid value for {path}. Expected {expected_type.__name__}.","RED")
                console.print()
                return

        SESSION_CONFIG[key] = value

        Print(f"Updated session-config {key} → {value}", "GREEN")
        console.print()
        return
    
    #.session-config reset
    if cmd == ".session-config reset":
        confirm = confirm_reset(
            "pydbms warning: This command will reset all fields in session-config to default values.\n"
            "Confirm reset (yes/no)?"
        )

        if not confirm:
            Print("Session-config reset aborted.", "GREEN")
            console.print()
            return

        SESSION_CONFIG.clear()
        SESSION_CONFIG.update(DEFAULT_SESSION_CONFIG)

        Print("All session-config values reset to default.", "GREEN")
        console.print()
        return
    
    # .session-config reset <key?>
    if cmd.startswith(".session-config reset "):
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
