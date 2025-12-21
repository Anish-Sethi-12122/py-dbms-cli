#Instance MySQL

from .dependencies import mysql, pwinput, sys, time, sqlparse, Panel, Table, re, box
from .Global import Print, console

def connect():
    try:
        host="localhost"
        user="root"
        Print(f"pydbms> Enter host name for MySQL (default value -> {host}):", "YELLOW")
        host=input()
        if not host:
            host="localhost"
        Print(f"pydbms> Enter user name for MySQL (default value -> {user}):", "YELLOW")
        user=input()
        if not user:
            user="root"
        Pas=pwinput.pwinput(prompt='pydbms> Enter password: ', mask='*')
    except KeyboardInterrupt:
        Print("Invalid", "RED", "bold")
        sys.exit()
        
    try:
        con = mysql.connect(host=host, user=user, passwd=Pas)
        cur = con.cursor()
        Print("✅ Login successful.\nSuccessfully connected to MySQL\n\n","GREEN")
        return con,cur
    except mysql.Error:
        Print("❌ Login failed: Incorrect password entered\n", "RED", "bold")
        sys.exit()
    return -1

def print_warnings(cur):
    warnings = cur.fetchwarnings()
    if warnings:
        for level, warning_code, warning_msg in warnings:
            Print(f"Warning [{warning_code}]: {warning_msg}", "YELLOW", "bold")
        console.print()
        return True
    return False

def execute_select(query,cur):
    start = time.time()
    cur.execute(query)
    end = time.time()
    result=cur.fetchall()
    num_rows=len(result)
    columns = [desc[0] for desc in cur.description]
    console.print()
    
    result_table = Table(show_header=True, box=box.SIMPLE_HEAVY, padding=(0,1))
    
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

def execute_change(query,con,cur):
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

def execute(query,cur):
    cur.execute(query)
    
    has_warning=print_warnings(cur)
    
    if has_warning:
        msg = "Query executed with warning."
    else:
        msg = "Query executed."
    
    Print(msg, "YELLOW" if has_warning else "GREEN")
    console.print()
    
def get_query_mysql():
    try:
        buffer = ""
        while True:
            line = input("pydbms> " if buffer == "" else "       ")
            buffer += line + "\n"
            if buffer.strip().startswith("."):
                break
            statements = sqlparse.parse(buffer)
            if statements and buffer.strip().endswith(";"):
                break
        query = buffer
            
    except KeyboardInterrupt:
        Print("Invalid", "RED", "bold")
        
    console.print()
    return query

def get_query_title(query):
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
