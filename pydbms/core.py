'''
PY DBMS — DB client CLI
Copyright (C) 2025  Anish Sethi
Licensed under - BSD-3-Clause License
Version - 3.1.0
Release - Release
'''

# pydbms/pydbms/main/core.py

from .runtime import Print, console, config
from .dependencies import pyfiglet, Text, Table, Align, Rule, Panel, mysql, sys, Group
from .pydbms_mysql import execute, execute_change, execute_select, get_query_mysql
from .pydbms_path import pydbms_path
from ..export.export_manager import ExportManager
from ..db.db_manager import connect_db
from .config import validate_config_types
from .query_parse_and_classify import parse_query, classify_rest, classify_query
from .meta_handler import meta

def print_banner() -> None:
    ascii_art = pyfiglet.figlet_format("PY   DBMS", font="slant").rstrip()
    
    logo = Text(ascii_art, style="bold color(57)") 
    
    banner_table = Table(show_header=False, box=None, expand=True)
    banner_table.add_column("1", justify="center", ratio=1)
    banner_table.add_column("2", justify="center", ratio=1)
    banner_table.add_column("3", justify="center", ratio=1)
    banner_table.add_column("4", justify="center", ratio=1)

    banner_table.add_row(
        "[bold cyan]v3.1.0[/]\n[bold white]Version[/]",
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
    
    console.print()
    console.print()
    
def main():
    config_validated = validate_config_types()
    config.clear()
    config.update(config_validated)

    if config["ui"].get("show_banner", True):
        print_banner()
    
    Print("\nWelcome to PY DBMS, a UI/UX focused CLI tool for your Database needs.\nNOTE that PY DBMS is a Database Client that provides an interface to access databases, and not a database manager itself.\n\n", "MAGENTA", slow_type=False)
    
    console.print()
    console.print()
    console.print()
    
    con, cur = connect_db.driver("mysql", config)
    
    while not con or not cur:
        try:
            con, cur = connect_db.driver("mysql", config)
            
        except Exception as e:
            Print(f"Error while trying to connect to DB - MySQL.\n {e}", "RED")
            console.print()
    
    Print("\n\nIf you are unsure where to start, here are some helper commands.\n\n", "YELLOW")
    meta(".help",cur)
    console.print()
    
    while True:
        query, rest = parse_query(get_query_mysql())
        query_type = classify_query(query)
        rest_flags = classify_rest(rest)

        console.print()
        
        if query.lower().strip() in ["exit;", "exit"]:
            Print("Session Terminated.", "RED", "bold")
            sys.exit()

        if query_type == "meta":
            meta(query.strip(), cur, con)
            continue

        try:
            if query_type == "select":
                if rest_flags["expand_flag"]["expand"]:
                    query = query.rstrip(";") + " --expand;"
                    
                result = execute_select(query, cur)
                
                if rest_flags["export_flag"]["export"]:
                    if not result or not result.rows:
                        Print("pydbms error. Couldn't export query.\nReason: No rows returned. Nothing to export", "RED")
                        console.print()
                        continue

                    try:
                        export_path = ExportManager.export(
                            fmt=rest_flags["export_flag"]["export_format"],
                            result=result,
                            path=(
                                pydbms_path(rest_flags["export_flag"]["export_path"])
                                if rest_flags["export_flag"]["export_path"]
                                else None
                            )
                        )

                        Print("Export successful. Exported query result to → ","GREEN")
                        Print(export_path, slow_type=False)
                        console.print()

                    except Exception as export_error:
                        Print(f"pydbms error. Couldn't export query.\nReason: {export_error}","RED",slow_type=False)
                        console.print()

            elif query_type == "change":
                execute_change(query, con, cur)

            else:
                execute(query, cur)

        except SyntaxError as se:
            Print(f"pydbms error. Couldn't export query.\nReason: {se}","RED",slow_type=False)
            console.print()

        except mysql.Error as err:
            Print(err.msg, "RED")
            console.print()

        except Exception as e:
            Print(f"Unexpected error: {e}", "RED")

if __name__=="__main__":
    main()
