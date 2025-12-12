'''
PY DBMS — DB client CLI
Copyright (C) 2025  Anish Sethi
Licensed under - BSD-3-Clause License
'''

from .Global import Print, console
from .dependencies import pyfiglet, Text, Table, Align, Rule, Panel, mysql, sys
from .pydbms_mysql import execute, execute_change, execute_select, connect, get_query_mysql

def print_banner():
    ascii_art = pyfiglet.figlet_format("PY   DBMS", font="slant").rstrip()
    
    logo = Text(ascii_art, style="bold color(57)") 
    
    stats_table = Table(show_header=False, box=None, expand=True)
    stats_table.add_column("1", justify="center", ratio=1)
    stats_table.add_column("2", justify="center", ratio=1)
    stats_table.add_column("3", justify="center", ratio=1)

    stats_table.add_row(
        "[bold cyan]v1.0[/]\n [bold white]Version[/]",
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

def meta(cmd, cur):
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
        info.add_row("Version", "v1.0")
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
        return

    # .exit
    if cmd == ".exit":
        Print("Session Terminated.", "RED", "bold")
        sys.exit()

    print(f"Unknown command: {cmd}\nCheck your manual that corresponds to helper commands.")

def main():
    print_banner()
    con,cur=connect()
    
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