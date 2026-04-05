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


# ── --row-limit flag tests ────────────────────────────────────────────

def test_classify_rest_row_limit_valid():
    flags = classify_rest("--row-limit 50")
    assert flags["row_limit_flag"]["row_limit"] == 50

def test_classify_rest_row_limit_one():
    flags = classify_rest("--row-limit 1")
    assert flags["row_limit_flag"]["row_limit"] == 1

def test_classify_rest_row_limit_missing_value():
    with pytest.raises(SyntaxError, match="incorrect usage for --row-limit"):
        classify_rest("--row-limit")

def test_classify_rest_row_limit_invalid_string():
    with pytest.raises(SyntaxError, match="invalid value for --row-limit"):
        classify_rest("--row-limit abc")

def test_classify_rest_row_limit_zero():
    with pytest.raises(SyntaxError, match="Must be a positive integer"):
        classify_rest("--row-limit 0")

def test_classify_rest_row_limit_negative():
    with pytest.raises(SyntaxError, match="Must be a positive integer"):
        classify_rest("--row-limit -5")

def test_classify_rest_row_limit_default_none():
    """When --row-limit is not used, default should be None."""
    flags = classify_rest("")
    assert flags["row_limit_flag"]["row_limit"] is None


# ── --include-query flag tests ────────────────────────────────────────

def test_classify_rest_include_query_default_off():
    """Default behavior: include_query is False when no flag is specified."""
    flags = classify_rest("")
    assert flags["include_query_flag"]["include_query"] is False

def test_classify_rest_include_query_enabled():
    """When --include-query flag is present, include_query is True."""
    flags = classify_rest("--include-query")
    assert flags["include_query_flag"]["include_query"] is True


# ── Combined flag composition tests ──────────────────────────────────

def test_classify_rest_all_flags_combined():
    """All flags together should parse correctly."""
    flags = classify_rest("--row-limit 10 --export csv --expand --include-query")
    assert flags["row_limit_flag"]["row_limit"] == 10
    assert flags["export_flag"]["export"] is True
    assert flags["export_flag"]["export_format"] == "csv"
    assert flags["expand_flag"]["expand"] is True
    assert flags["include_query_flag"]["include_query"] is True

def test_classify_rest_row_limit_with_expand():
    flags = classify_rest("--expand --row-limit 25")
    assert flags["expand_flag"]["expand"] is True
    assert flags["row_limit_flag"]["row_limit"] == 25

