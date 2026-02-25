# tests/test_config.py
from pydbms.main.config import parse_query_config, get_default_value_config

def test_parse_query_config_valid():
    # Verifying the `section.key` semantic parser splits accurately
    assert parse_query_config("ui.max_rows") == ("ui", "max_rows")
    assert parse_query_config("export.path") == ("export", "path")

def test_parse_query_config_invalid():
    # Should catch and explicitly return None if there is no boundary separator mapping
    assert parse_query_config("uimax_rows") is None
    assert parse_query_config("export_path") is None

def test_get_default_value_config_valid():
    assert get_default_value_config("ui", "max_rows") == 1000
    assert get_default_value_config("mysql", "port") == 3306
    assert get_default_value_config("ui", "show_banner") is True

def test_get_default_value_config_invalid():
    # Looking for a completely fake dictionary tree sector
    assert get_default_value_config("fake_section", "fake_key") is None
    # Looking for a fake key in a REAL sector
    assert get_default_value_config("ui", "fake_key") is None
