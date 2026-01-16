# pydbms/pydbms/main/pydbms_mysql.py

from .dependencies import time, Panel, Table, re, box, dataclass, List, Any
from .runtime import Print, console, config
from .config import expand_query_session_config_mapping as Overflow

def get_query_mysql() -> str:
    try:
        lines = []

        while True:
            prompt = "pydbms> " if not lines else "       "
            line = input(prompt)
            lines.append(line)

            stripped = line.strip()

            if stripped.startswith("."):
                break
            
            if semicolon_in_query(line):
                break

        console.print()
        return "\n".join(lines)

    except KeyboardInterrupt:
        raise

def semicolon_in_query(line: str) -> bool:
    in_single = False
    in_double = False

    for ch in line:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == ";" and not in_single and not in_double:
            return True

    return False

def print_warnings(cur: object) -> bool:
    warnings = cur.fetchwarnings()
    if warnings:
        for level, warning_code, warning_msg in warnings:
            Print(f"Warning [{warning_code}]: {warning_msg}", "YELLOW", "bold")
        console.print()
        return True
    return False

def execute_select(query: str,cur: object) -> tuple[int, tuple[object,object, str, str, str] | list[tuple[object,object, str, str, str]], list] | None:    
    start = time.perf_counter()
    cur.execute(query)
    end = time.perf_counter()
    
    if config["ui"]["max_rows"] is None:
        result=cur.fetchall()
    else:
        result=cur.fetchmany(config["ui"]["max_rows"])
        
    num_rows=len(result)
    columns = [desc[0] for desc in cur.description]
    console.print()
    
    result_table = Table(show_header=True, box=box.SIMPLE_HEAVY, padding=(0,1))
    
    if "--expand" not in query:
        for i in columns:
            result_table.add_column(i, style="white", overflow=Overflow())
    else:
        for i in columns:
            result_table.add_column(i, style="white", no_wrap=True)

    for row in result:
        row_row = []
        for x in row:
            if x is None:  
                row_row.append("[dim white]NULL[/]")
            else:
                row_row.append(str(x))
        result_table.add_row(*row_row)

    title = get_query_title(query)
    
    console.print(
        Panel(
            result_table,
            title=title,
            border_style="bright_magenta",
            padding=(1, 2),
            expand=False
        )
    )
    
    has_warning = print_warnings(cur)

    if has_warning:
        msg = f"Query completed with warnings in {end-start:.3f} sec. Returned {num_rows} rows"
    else:
        msg = f"Query executed in {end-start:.3f}sec. Returned {num_rows} rows"
        
    console.print()
    Print(msg, "YELLOW" if has_warning else "GREEN")
    console.print()
    
    return QueryResult(query=query,columns=columns,rows=result)

def execute_change(query: str,con: object,cur: object) -> None:
    cur.execute(query)
    affected_row_num=cur.rowcount
    con.commit()
    
    has_warning=print_warnings(cur)
    
    if affected_row_num == 1:
        msg = "1 row affected."
    else:
        msg = f"{affected_row_num} rows affected."

    Print(msg, "YELLOW" if has_warning else "GREEN")
    console.print()

def execute(query: str,cur: object) -> None:
    cur.execute(query)
    
    has_warning=print_warnings(cur)
    
    if has_warning:
        msg = "Query executed with warning."
    else:
        msg = "Query executed."
    
    Print(msg, "YELLOW" if has_warning else "GREEN")
    console.print()
    

def get_query_title(query: str) -> str:
    q = query.strip().lower()

    # === Simple SELECT ===
    if q.startswith("select"):
        m = re.search(r"from\s+`?([a-zA-Z0-9_]+)`?", q)
        return m.group(1) if m else "Query Result"

    # === EXPLAIN ===
    if q.startswith("explain analyze"):
        return "Execution Analysis"
    if q.startswith("explain"):
        return "Query Execution Plan"

    # === DESCRIBE / SHOW COLUMNS ===
    m = re.match(r"(describe|desc|show columns from)\s+([a-zA-Z0-9_]+)", q)
    if m:
        return f"Description for table {m.group(2)}"

    # === SHOW CREATE ===
    m = re.match(r"show create (\w+)\s+([a-zA-Z0-9_]+)", q)
    if m:
        kind, name = m.group(1), m.group(2)
        return f"Create {kind.capitalize()}: {name}"

    # === Generic SHOW commands ===
    show_map = {
        "show tables": "List of Tables in current database",
        "show full tables": "List of Tables (Extended) in current database",
        "show databases": "List of Databases in current connection",
        "show schemas": "List of Databases",
        "show triggers": "Triggers",
        "show events": "Events",
        "show plugins": "Plugins",
        "show privileges": "Privileges",
        "show processlist": "Process List",
        "show engines": "Storage Engines",
        "show character set": "Character Sets",
        "show collation": "Collations",
        "show variables": "Server Variables",
        "show global status": "Global Status Variables",
        "show session status": "Session Status Variables",
        "show engine innodb status": "InnoDB Engine Status",
    }

    for key, title in show_map.items():
        if q.startswith(key):
            return title

    # === HELP ===
    if q.startswith("help"):
        return f"Help: {query[4:].strip()}"

    return "Query Result"

@dataclass
class QueryResult:
    query: str
    columns: List[str]
    rows: List[List[Any]]

