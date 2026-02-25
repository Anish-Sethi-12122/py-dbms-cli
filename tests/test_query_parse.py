import pytest
from pydbms.main.query_parse_and_classify import (
    parse_query_and_flags,
    classify_query,
    classify_rest
)

def test_parse_query_and_flags_basic():
    sql, rest = parse_query_and_flags("SELECT * FROM users; --expand")
    assert sql == "SELECT * FROM users;"
    assert rest == "--expand"

def test_parse_query_multiple_semicolons():
    # It parses until the FIRST unescaped/unquoted semicolon it finds.
    sql, rest = parse_query_and_flags("SELECT * FROM foo; SELECT * FROM bar;")
    assert sql == "SELECT * FROM foo;"
    assert rest == "SELECT * FROM bar;"

def test_parse_query_escaped_strings():
    sql, rest = parse_query_and_flags("SELECT ';', \"hello;\" FROM users; --export json")
    assert sql == "SELECT ';', \"hello;\" FROM users;"
    assert rest == "--export json"

def test_classify_query():
    assert classify_query(".help") == "meta"
    assert classify_query("  SELECT * FROM test ") == "select"
    assert classify_query("update users set name='hi' ") == "change"
    assert classify_query("DROP TABLE users;") == "ddl"
    assert classify_query("some random stuff") == "other"

def test_classify_rest_empty():
    flags = classify_rest("")
    assert flags["expand_flag"]["expand"] is False
    assert flags["export_flag"]["export"] is False

def test_classify_rest_expand():
    flags = classify_rest("--expand")
    assert flags["expand_flag"]["expand"] is True
    assert flags["export_flag"]["export"] is False

def test_classify_rest_export_no_path():
    flags = classify_rest("--export json")
    assert flags["export_flag"]["export"] is True
    assert flags["export_flag"]["export_format"] == "json"
    assert flags["export_flag"]["export_path"] is None

def test_classify_rest_export_with_path():
    flags = classify_rest('--export csv "C:/My Data/data.csv"')
    assert flags["export_flag"]["export"] is True
    assert flags["export_flag"]["export_format"] == "csv"
    assert flags["export_flag"]["export_path"] == "C:/My Data/data.csv"

def test_classify_rest_unsupported_syntax():
    with pytest.raises(SyntaxError, match="incorrect usage for export"):
        classify_rest("--export")

    with pytest.raises(SyntaxError, match="Unknown flag"):
        classify_rest("--fakeflag")
