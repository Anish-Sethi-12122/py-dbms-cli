# tests/test_export_manager.py
import os
import pytest
from pydbms.export.export_manager import ExportManager

def test_default_export_dir():
    # Because `pydbms_path` dynamically resolves to AppData on Windows or ~/.config on Unix,
    # we just need to ensure it returns a valid string ending in "exports"
    dir_path = ExportManager.default_export_dir()
    assert isinstance(dir_path, str)
    assert dir_path.endswith("exports") or dir_path.endswith("exports/") or dir_path.endswith("exports\\")

def test_resolve_export_path_no_path():
    # If no path is provided, it should generate a default timestamped filename
    path = ExportManager.resolve_export_path(None, "json")
    assert path.endswith(".json")
    assert "pydbms-export" in path

def test_normalize_export_dir_valid(tmp_path):
    # pytest provides `tmp_path` which is an isolated temporary directory
    valid_dir = str(tmp_path / "my_exports")
    
    # Should create the directory and return it
    resolved = ExportManager.normalize_export_dir(valid_dir)
    assert resolved == valid_dir
    assert os.path.isdir(valid_dir)

def test_normalize_export_dir_invalid_file_extension():
    with pytest.raises(ValueError, match="must be a DIRECTORY"):
        ExportManager.normalize_export_dir("C:/my_folder/file.csv")

def test_normalize_export_dir_empty_string():
    with pytest.raises(ValueError, match="non-empty directory path"):
        ExportManager.normalize_export_dir("   ")

def test_export_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported export format"):
        # We pass None for 'result' since it shouldn't reach the exporter instantiation
        ExportManager.export("pdf", None)


# ── include_query export tests ────────────────────────────────────────

class MockQueryResult:
    """Minimal QueryResult stand-in for export tests."""
    def __init__(self, query="SELECT * FROM test;", columns=None, rows=None):
        self.query = query
        self.columns = columns or ["id", "name"]
        self.rows = rows or [[1, "Alice"], [2, "Bob"]]


def test_export_csv_includes_query(tmp_path):
    """When include_query=True, CSV should have a comment row with the SQL query."""
    result = MockQueryResult()
    out = str(tmp_path / "test_with_query.csv")

    ExportManager.export("csv", result, path=out, include_query=True)

    with open(out, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.startswith("# SELECT * FROM test;")
    assert "id,name" in content
    assert "Alice" in content


def test_export_csv_excludes_query(tmp_path):
    """When include_query=False, CSV should NOT contain the SQL comment row."""
    result = MockQueryResult()
    out = str(tmp_path / "test_no_query.csv")

    ExportManager.export("csv", result, path=out, include_query=False)

    with open(out, "r", encoding="utf-8") as f:
        content = f.read()

    assert not content.startswith("#")
    assert "id,name" in content


def test_export_json_includes_query(tmp_path):
    """When include_query=True, JSON should have a 'query' key wrapping the rows."""
    import json
    result = MockQueryResult()
    out = str(tmp_path / "test_with_query.json")

    ExportManager.export("json", result, path=out, include_query=True)

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, dict)
    assert "query" in data
    assert data["query"] == "SELECT * FROM test;"
    assert "rows" in data
    assert len(data["rows"]) == 2


def test_export_json_excludes_query(tmp_path):
    """When include_query=False, JSON should be a flat array of row objects."""
    import json
    result = MockQueryResult()
    out = str(tmp_path / "test_no_query.json")

    ExportManager.export("json", result, path=out, include_query=False)

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Alice"

