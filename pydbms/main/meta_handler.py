# pydbms/pydbms/main/meta_handler.py

from .dependencies import Table, Panel
import sys
import copy
from ..db.db_exceptions import DatabaseError
from .runtime import Print, PrintNewline, config, console, ver
from .pydbms_mysql import execute_select
from ..export.export_manager import ExportManager
from ..engine.engine_base import pydbms_error, pydbms_warning  # Centralized UX helpers
from ..db.db_errors import MySQLErrors  # DB-engine-specific error output
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
        PrintNewline()
        
        PrintNewline()
        help_table = Table(title="Helper Flags", show_header=False, border_style="bold magenta")
        help_table.add_column("Flag Usage", overflow="ellipsis")
        help_table.add_column("Description", style="white", no_wrap=True)
        help_table.add_row("--expand", "Show full cell value without wrap (overrides session-config)")
        help_table.add_row("--export <format> <path?>", "Export a query result. Supports -> csv, json")
        help_table.add_row("--row-limit <N>", "Limit rows returned for this query (overrides ui.max_rows)")
        help_table.add_row("--include-query", "Embed original SQL query in exported file (default: off)")
        console.print(help_table)
        PrintNewline()
        return

    # .databases
    if cmd == ".databases":
        try:
            execute_select("SHOW DATABASES;",cur)
            
        except DatabaseError as err:
            MySQLErrors.error(str(err))
            PrintNewline()
            
        return
            
    # .tables
    if cmd == ".tables":
        try:
            execute_select("SHOW TABLES;",cur)
            
        except DatabaseError as err:
            MySQLErrors.error(str(err))
            PrintNewline()
            
        return

    # .schema table_name
    if cmd.startswith(".schema"):
        parts = cmd.split()
        
        if len(parts) != 2:
            pydbms_warning("Usage: .schema <table_name>")
            PrintNewline()
            return
        table = parts[1]
        
        try:
            cur.execute(f"SHOW CREATE TABLE {table};")
            row = cur.fetchone()
            if row:
                Print(row[1] + "\n", slow_type=False)
                PrintNewline()
            else:
                MySQLErrors.error(f"No such table: {table}")
                
        except DatabaseError as err:
            MySQLErrors.error(str(err))
            PrintNewline()
            
        return

    # .clear
    if cmd == ".clear":
        import os
        os.system("cls" if os.name == "nt" else "clear")
        PrintNewline()
        return
    
    # .version
    if cmd == ".version":
        PrintNewline()
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
        PrintNewline()
        Print("Run `pip install -U py-dbms-cli` in terminal to check for updates.\n\n", "WHITE")
        Print("NOTE: Run `pip install --upgrade py-dbms-cli` in terminal directly to install the latest version.\n", "WHITE")
        PrintNewline()
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
        
        export_cfg = config.get("export", {})
        outer.add_row("Export", build_section_table(export_cfg))
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
        PrintNewline()
        return

    # .config set
    if cmd.startswith(".config set"):
        parts = cmd.split(maxsplit=3)

        if len(parts) != 4:
            pydbms_error("Invalid input format.")
            pydbms_warning("Usage: .config set <section>.<key> <value>")
            PrintNewline()
            return

        _, _, path, raw_value = parts

        parsed = parse_query_config(path)
        if not parsed:
            pydbms_error("Invalid input format. Use <section>.<key>")
            PrintNewline()
            return

        section, key = parsed
        section = section.lower()
        key = key.lower()

        if section not in config or key not in config[section]:
            pydbms_error(f"Unknown config key: {path}")
            PrintNewline()
            return

        try:
            val_lower = raw_value.strip().lower()

            if section == "ui" and key == "show_banner":
                if val_lower in ("true", "1", "yes", "on"):
                    value = True
                elif val_lower in ("false", "0", "no", "off"):
                    value = False
                else:
                    raise ValueError("Expected boolean (true/false)")

            elif section == "ui" and key == "max_rows":
                if val_lower in ("none", "null"):
                    value = None
                else:
                    value = int(raw_value)
                    if value < 1:
                        raise ValueError("Must be a positive integer")

            elif section == "mysql" and key == "port":
                value = int(raw_value)

            elif section == "mysql" and key in ("host", "user", "database"):
                if val_lower in ("none", "null"):
                    value = None
                else:
                    value = raw_value

            elif section == "export" and key == "path":
                value = raw_value # ExportManager.normalize checks this immediately after.

            else:
                # Fallback for unknown keys (shouldn't really happen if config dict is strict)
                value = raw_value

        except ValueError as err:
            pydbms_error(f"Invalid value for {path}.\nReason: {err}")
            PrintNewline()
            return
        except Exception:
            pydbms_error(f"Invalid value for {path}.")
            PrintNewline()
            return
        
        if section == "export" and key == "path":
            try:
                value = ExportManager.normalize_export_dir(str(value))
            except Exception as e:
                pydbms_error(f"Invalid value for export.path.\nReason: {e}")
                PrintNewline()
                return

        config[section][key] = value
        save_config(config)

        Print(f"Updated {path} → {value}", "GREEN")
        PrintNewline()
        return
    
    #.config reset
    if cmd == ".config reset":
        pydbms_warning("This command will reset all fields in config to default values.")
        
        confirm = confirm_reset("Confirm reset (yes/no): ")

        if not confirm:
            Print("Config reset aborted.\n", "GREEN")
            PrintNewline()
            return

        config.clear()
        config.update(copy.deepcopy(DEFAULT_CONFIG))
        save_config(config)

        Print("All config values reset to default.\n", "GREEN")
        PrintNewline()
        return
    
    # .config reset <key?>
    if cmd.startswith(".config reset"):
        parts = cmd.split(maxsplit=2)

        if len(parts) != 3:
            pydbms_error("Invalid config key format.")
            pydbms_warning("Usage: .config reset <section>.<key>")
            PrintNewline()
            return

        path = parts[2]
        parsed = parse_query_config(path)

        if not parsed:
            pydbms_error("Invalid config key format. Use <section>.<key>")
            PrintNewline()
            return

        section, key = parsed
        section = section.lower()
        key = key.lower()

        default = get_default_value_config(section, key)
        if default is None:
            pydbms_error(f"No default value for {path}.")
            PrintNewline()
            return

        config[section][key] = default
        save_config(config)

        Print(f"Reset {path} → {default}\n", "GREEN")
        PrintNewline()
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

        PrintNewline()
        return
    
    # .session-config set
    if cmd.startswith(".session-config set"):
        parts = cmd.split(maxsplit=3)

        if len(parts) != 4:
            pydbms_error("Invalid input format.")
            pydbms_warning("Usage: .session-config set <key> <value>")
            PrintNewline()
            return

        _, _, key, raw_value = parts
        key = key.lower()

        if key not in SESSION_CONFIG:
            pydbms_error(f"Unknown session config key: {key}")
            PrintNewline()
            return

        try:
            val_lower = raw_value.strip().lower()

            # Right now, expand-query-result is the only session config key
            if key == "expand-query-result":
                if val_lower in ("true", "1", "yes", "on"):
                    value = True
                elif val_lower in ("false", "0", "no", "off"):
                    value = False
                else:
                    raise ValueError("Expected boolean (true/false)")
            else:
                # Fallback for future unhandled keys
                value = raw_value

        except ValueError as err:
            pydbms_error(f"Invalid value for {key}.\nReason: {err}")
            PrintNewline()
            return
        except Exception:
            pydbms_error(f"Invalid value for {key}.")
            PrintNewline()
            return

        SESSION_CONFIG[key] = value

        Print(f"Updated session-config {key} → {value}\n", "GREEN")
        PrintNewline()
        return
    
    #.session-config reset
    if cmd == ".session-config reset":
        confirm = confirm_reset(
            "pydbms warning> This command will reset all fields in session-config to default values.\n"
            "Confirm reset (yes/no)?"
        )

        if not confirm:
            Print("Session-config reset aborted.\n", "GREEN")
            PrintNewline()
            return

        SESSION_CONFIG.clear()
        SESSION_CONFIG.update(DEFAULT_SESSION_CONFIG)

        Print("All session-config values reset to default.\n", "GREEN")
        PrintNewline()
        return
    
    # .session-config reset <key?>
    if cmd.startswith(".session-config reset "):
        parts = cmd.split(maxsplit=2)

        if len(parts) != 3:
            pydbms_error("Invalid input format.")
            pydbms_warning("Usage: .session-config reset <key>")
            PrintNewline()
            return

        key = parts[2].lower()

        if key not in DEFAULT_SESSION_CONFIG:
            pydbms_error(f"Unknown session config key: {key}")
            PrintNewline()
            return

        SESSION_CONFIG[key] = DEFAULT_SESSION_CONFIG[key]

        Print(f"Reset session-config {key} → {DEFAULT_SESSION_CONFIG[key]}\n", "GREEN")
        PrintNewline()
        return

    # .exit   
    if cmd == ".exit" or cmd == ".exit;":
        Print("\n\nSession Terminated.\n", "RED", "bold")
        PrintNewline()
        
        if con:
                try:
                    cur.close()
                    con.close()
                except Exception:
                    pass
                
        sys.exit()

    pydbms_error(f"Unknown command: {cmd}\nRefer to `.help` for list of commands")
    PrintNewline()