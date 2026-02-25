'''
PY DBMS — DB client CLI
Copyright (C) 2025  Anish Sethi
Licensed under - BSD-3-Clause License
Version - 4.0.0
Release - Experimental
'''

# pydbms/pydbms/main/core.py

from .runtime import Print, console, config
from .dependencies import pyfiglet, Text, Table, Align, Rule, Panel, mysql, Group
from .pydbms_mysql import execute_query, execute_change, execute_select, get_query_mysql
from ..export.export_manager import ExportManager
from ..db.db_manager import connect_db
from ..db.db_exceptions import DatabaseError
from .config import validate_config_types
from .query_parse_and_classify import parse_query_and_flags, classify_rest, classify_query
from .meta_handler import meta
from ..profile.profile_auth import ensure_local_profile_login

def print_banner() -> None:
    ascii_art = pyfiglet.figlet_format("PY   DBMS", font="slant").rstrip()

    logo = Text(ascii_art, style="bold color(57)")

    banner_table = Table(show_header=False, box=None, expand=True)
    banner_table.add_column("1", justify="center", ratio=1)
    banner_table.add_column("2", justify="center", ratio=1)

    banner_table.add_row(
        "[bold yellow]MySQL[/]\n[bold white]Currently Supported[/]",
        "[bold green]Online since 2025[/]\n[bold white]Status[/]"
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
        
    ensure_local_profile_login()

    Print("\nWelcome to PY DBMS, a UI/UX focused CLI tool for your Database needs.\nNOTE that PY DBMS is a Database Client that provides an interface to access databases, and not a database manager itself.\n\n","MAGENTA",slow_type=False)

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
    meta(".help", cur)
    console.print()

    while True:
        raw_query = get_query_mysql()

        query, rest = parse_query_and_flags(raw_query)
        query_type = classify_query(query)

        console.print()

        if query_type == "meta":
            meta(query.strip(), cur, con)
            continue

        try:
            rest_flags = classify_rest(rest)

            result = None

            if query_type == "select":
                result = execute_select(
                    query,
                    cur,
                    expand=rest_flags["expand_flag"]["expand"]
                )

            elif query_type in ("change", "ddl"):
                result = execute_change(
                    query,
                    con,
                    cur,
                    expand=rest_flags["expand_flag"]["expand"]
                )

            else:
                result = execute_query(
                    query,
                    con,
                    cur,
                    expand=rest_flags["expand_flag"]["expand"]
                )

            if rest_flags["export_flag"]["export"]:
                if not result or not result.rows:
                    Print("pydbms error> Couldn't export query.\nReason: No rows returned. Nothing to export\n", "RED")
                    console.print()
                    continue

                try:
                    export_path = ExportManager.export(
                        fmt=(rest_flags["export_flag"]["export_format"]),
                        result=result,
                        path=(rest_flags["export_flag"]["export_path"] or config.get("export", {}).get("path") or None)
                    )

                    Print("Export successful. Exported query result to → ", "GREEN")
                    Print(f"{export_path}\n", slow_type=False)
                    console.print()

                except Exception as export_error:
                    Print(f"pydbms error> Couldn't export query.\nReason: {export_error}\n", "RED", slow_type=False)

        except SyntaxError as se:
            Print(f"pydbms error> Invalid flag usage.\nReason: {se}\n", "RED", slow_type=False)
            console.print()

        except mysql.Error as err:
            Print(f"mysql error> {err.msg}\n", "RED")
            console.print()
            
        except DatabaseError as err:
            Print(f"mysql error> {str(err)}\n", "RED")
            console.print()
            
        except Exception as e:
            Print(f"pydbms error> Unexpected error: {e}\n", "RED")
            console.print()

        console.print()


if __name__ == "__main__":
    main()
