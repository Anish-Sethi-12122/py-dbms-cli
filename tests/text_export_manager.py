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
