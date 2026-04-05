# pydbms/pydbms/main/query_parse_and_classify.py

import shlex
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedQuery:
    """Structured representation of a parsed query and its inline flags."""
    sql: str
    flags: dict = field(default_factory=dict)


def parse_query_and_flags(raw: str) -> tuple[str, Optional[str]]:
    """Split a raw input string into (sql, rest) at the first unquoted semicolon.

    Returns:
        Tuple of (sql_string, remaining_flags_string_or_None).
    """
    in_single: bool = False
    in_double: bool = False
    escape: bool = False

    for i, ch in enumerate(raw):
        if escape:
            escape = False
            continue

        if ch == "\\":
            escape = True
            continue

        if ch == "'" and not in_double:
            in_single = not in_single
            continue

        if ch == '"' and not in_single:
            in_double = not in_double
            continue

        if ch == ";" and not in_single and not in_double:
            sql = raw[: i + 1].strip()
            rest = raw[i + 1 :].strip()
            return sql, rest if rest else None

    return raw.strip(), None


def classify_query(query: str) -> str:
    """Classify a query string into a category for execution routing.

    Returns one of: "meta", "select", "change", "ddl", "other".
    """
    q = query.strip().lower()

    if q.startswith("."):
        return "meta"

    if q.startswith(("select", "with", "show", "desc", "describe", "explain")):
        return "select"

    if q.startswith(("insert", "update", "delete")):
        return "change"

    if q.startswith(("create", "drop", "alter", "truncate")):
        return "ddl"

    return "other"


def classify_rest(rest: Optional[str]) -> dict:
    """Parse the flag portion (after the semicolon) into a structured flags dict.

    Supported flags:
        --expand                        Override session column wrapping
        --export <format> <path?>       Export query result to file
        --row-limit <N>                 Limit rows returned (overrides ui.max_rows)
        --include-query                 Embed original SQL query in export file

    Returns:
        dict with keys: export_flag, expand_flag, row_limit_flag, include_query_flag.
    """
    flags: dict = {
        "export_flag": {
            "export": False,
            "export_format": None,
            "export_path": None,
        },
        "expand_flag": {
            "expand": False,
        },
        "row_limit_flag": {
            "row_limit": None,      # None = use config default; int = override
        },
        "include_query_flag": {
            "include_query": False,  # Default OFF — user must opt in with --include-query
        },
    }

    if not rest:
        return flags

    tokens: list[str] = shlex.split(rest)
    i: int = 0

    while i < len(tokens):
        token: str = tokens[i]

        # ── --expand ──────────────────────────────────────────────
        if token == "--expand":
            flags["expand_flag"]["expand"] = True
            i += 1
            continue

        # ── --export <format> <path?> ─────────────────────────────
        if token == "--export":
            flags["export_flag"]["export"] = True

            if i + 1 >= len(tokens):
                raise SyntaxError(
                    "incorrect usage for export query.\n"
                    "Usage: <query> --export <format> <path?>"
                )

            flags["export_flag"]["export_format"] = tokens[i + 1]

            if i + 2 < len(tokens) and not tokens[i + 2].startswith("--"):
                flags["export_flag"]["export_path"] = tokens[i + 2]
                i += 3
            else:
                i += 2

            continue

        # ── --row-limit <N> ───────────────────────────────────────
        if token == "--row-limit":
            if i + 1 >= len(tokens):
                raise SyntaxError(
                    "incorrect usage for --row-limit.\n"
                    "Usage: <query> --row-limit <positive integer>"
                )

            raw_value: str = tokens[i + 1]

            try:
                limit = int(raw_value)
            except ValueError:
                raise SyntaxError(
                    f"invalid value for --row-limit: '{raw_value}'.\n"
                    "Expected a positive integer."
                )

            if limit < 1:
                raise SyntaxError(
                    f"invalid value for --row-limit: {limit}.\n"
                    "Must be a positive integer (>= 1)."
                )

            flags["row_limit_flag"]["row_limit"] = limit
            i += 2
            continue

        # ── --include-query ────────────────────────────────────────
        if token == "--include-query":
            flags["include_query_flag"]["include_query"] = True
            i += 1
            continue

        raise SyntaxError(f"Unknown flag: {token}")

    return flags
