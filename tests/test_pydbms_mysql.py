# tests/test_pydbms_mysql.py
from pydbms.main.pydbms_mysql import semicolon_in_query, get_query_title

def test_semicolon_in_query_basic():
    assert semicolon_in_query("SELECT * FROM users;") is True
    assert semicolon_in_query("SELECT * FROM users") is False

def test_semicolon_in_query_ignored_in_quotes():
    # Semicolons inside strings should be ignored to prevent false-positives
    assert semicolon_in_query("SELECT ';' FROM dual") is False
    assert semicolon_in_query('SELECT ";" FROM dual') is False
    assert semicolon_in_query("SELECT ';' FROM dual;") is True

def test_get_query_title_select():
    assert get_query_title("SELECT * FROM users LIMIT 10") == "users"
    assert get_query_title("SELECT id FROM `logs`") == "logs"

def test_get_query_title_explain():
    assert get_query_title("EXPLAIN SELECT * FROM users") == "Query Execution Plan"
    assert get_query_title("EXPLAIN ANALYZE SELECT * FROM users") == "Execution Analysis"

def test_get_query_title_show_commands():
    assert get_query_title("SHOW TABLES") == "List of Tables in current database"
    assert get_query_title("SHOW DATABASES") == "List of Databases in current connection"
    assert get_query_title("SHOW CREATE TABLE users") == "Create Table: users"

def test_get_query_title_generic():
    # If it falls through every regex bucket, it just prints a standard text block
    assert get_query_title("INSERT INTO users VALUES (1)") == "Query Result"
