# pydbms/pydbms/main/pydbms_mysql.py
# MySQL-specific query execution, result rendering, and cursor utilities.

from .dependencies import Panel, Table, box
from dataclasses import dataclass
from typing import List, Any, Optional
import time
import re
from .runtime import Print, PrintNewline, console, config
from .config import expand_query_session_config_mapping as Overflow
from ..db.db_errors import MySQLErrors  # Centralized MySQL error/warning output


@dataclass
class QueryResult:
    query: str
    columns: List[str]
    rows: List[List[Any]]


def get_query_mysql() -> str:
    try:
        lines = []
        while True:
            prompt = "pydbms> " if not lines else "    -> "
            line = input(prompt)
            lines.append(line)
            stripped = line.strip()

            accumulated = "\n".join(lines)

            if stripped.startswith("."):
                break

            if semicolon_in_query(accumulated):
                break

        PrintNewline()
        return accumulated

    except KeyboardInterrupt:
        raise

def semicolon_in_query(query: str) -> bool:
    in_single = False
    in_double = False

    for ch in query:
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
            MySQLErrors.warning(f"Warning [{warning_code}]: {warning_msg}")
        PrintNewline()
        return True
    return False


def query_returns_rows(cur: object) -> bool:
    return cur.description is not None


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


def render_cursor_result(
    query: str,
    cur: object,
    *,
    start: float,
    end: float,
    expand: bool = False,
    row_limit: Optional[int] = None,
) -> QueryResult:
    """Render a cursor result set as a rich Panel table.

    Args:
        query: The original SQL query string (used for title extraction).
        cur: Active database cursor with a pending result set.
        start: Perf counter timestamp when execution began.
        end: Perf counter timestamp when execution finished.
        expand: If True, columns are rendered without text wrapping.
        row_limit: If provided, overrides the persistent ui.max_rows config
                   for this single query. None = use config default.
    """
    # --row-limit flag takes precedence over config default
    max_rows: Optional[int] = row_limit if row_limit is not None else config["ui"]["max_rows"]

    if max_rows is None:
        rows = cur.fetchall()
    else:
        rows = cur.fetchmany(max_rows)
        drain_remaining_rows(cur)

    num_rows = len(rows)
    columns = [desc[0] for desc in cur.description] if cur.description else []

    PrintNewline()
    result_table = Table(show_header=True, box=box.SIMPLE_HEAVY, padding=(0, 1))

    for col in columns:
        if expand:
            result_table.add_column(col, style="white", no_wrap=True)
        else:
            result_table.add_column(col, style="white", overflow=Overflow())

    for row in rows:
        result_table.add_row(*("[dim white]NULL[/]" if x is None else str(x) for x in row))

    title = get_query_title(query)

    console.print(
        Panel(
            result_table,
            title=title,
            border_style="bright_magenta",
            padding=(1, 2),
            expand=False,
        )
    )

    has_warning = print_warnings(cur)
    PrintNewline()

    msg = (
        f"Query completed with warnings in {end-start:.3f} sec. Returned {num_rows} rows"
        if has_warning
        else f"Query executed in {end-start:.3f} sec. Returned {num_rows} rows"
    )

    Print(msg + "\n", "YELLOW" if has_warning else "GREEN")
    PrintNewline()

    return QueryResult(query=query, columns=columns, rows=rows)

def drain_remaining_rows(cur: object, chunk_size: int = 2048) -> None:
    try:
        while True:
            chunk = cur.fetchmany(chunk_size)
            if not chunk:
                break
    except Exception:
        pass

def execute_select(
    query: str,
    cur: object,
    *,
    expand: bool = False,
    row_limit: Optional[int] = None,
) -> Optional[QueryResult]:
    """Execute a SELECT-type query and render the result table.

    Args:
        row_limit: Override for ui.max_rows this query only. None = use config.
    """
    start = time.perf_counter()
    with console.status("[bold cyan]Executing query...[/]", spinner="dots"):
        cur.execute(query)
    end = time.perf_counter()

    if not query_returns_rows(cur):
        Print("Query executed but returned no resultset.\n", "YELLOW")
        PrintNewline()
        return None

    return render_cursor_result(query, cur, start=start, end=end, expand=expand, row_limit=row_limit)


def execute_change(
    query: str,
    con: object,
    cur: object,
    *,
    expand: bool = False,
    row_limit: Optional[int] = None,
) -> Optional[QueryResult]:
    """Execute a DML (INSERT/UPDATE/DELETE) or DDL query, commit, and render results.

    Args:
        row_limit: Override for ui.max_rows this query only. None = use config.
    """
    start = time.perf_counter()
    with console.status("[bold cyan]Executing query...[/]", spinner="dots"):
        cur.execute(query)
    end = time.perf_counter()

    if query_returns_rows(cur):
        return render_cursor_result(query, cur, start=start, end=end, expand=expand, row_limit=row_limit)

    try:
        con.commit()
    except Exception:
        pass

    has_warning = print_warnings(cur)

    affected = getattr(cur, "rowcount", -1)
    if affected is None:
        affected = -1

    if affected >= 0:
        msg = f"Query OK, {affected} rows affected ({end-start:.3f} sec)"
    else:
        msg = f"Query OK ({end-start:.3f} sec)"

    Print(msg + "\n", "YELLOW" if has_warning else "GREEN")
    PrintNewline()
    return None


def execute_query(
    query: str,
    con: object,
    cur: object,
    *,
    expand: bool = False,
    row_limit: Optional[int] = None,
) -> Optional[QueryResult]:
    """Execute a generic query, commit if needed, and render any result set.

    Args:
        row_limit: Override for ui.max_rows this query only. None = use config.
    """
    start = time.perf_counter()
    with console.status("[bold cyan]Executing query...[/]", spinner="dots"):
        cur.execute(query)
    end = time.perf_counter()

    if query_returns_rows(cur):
        return render_cursor_result(query, cur, start=start, end=end, expand=expand, row_limit=row_limit)

    try:
        con.commit()
    except Exception:
        pass

    has_warning = print_warnings(cur)

    msg = (
        f"Query executed with warning in {end-start:.3f} sec."
        if has_warning
        else f"Query executed in {end-start:.3f} sec."
    )

    Print(msg + "\n", "YELLOW" if has_warning else "GREEN")
    PrintNewline()
    return None