# pydbms/pydbms/main/query_parse_and_classify.py

from .dependencies import shlex

def parse_query(raw: str) -> tuple[str, str | None]:
    if ";" not in raw:
        return raw.strip(), None

    head, sep, tail = raw.partition(";")
    core = head.strip() + ";"
    rest = tail.strip()

    return core, rest if rest else None


def classify_query(query: str) -> str:
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


def classify_rest(rest: str | None) -> dict:
    flags = {
        "export_flag": {
            "export": False,
            "export_format": None,
            "export_path": None,
        },
        "expand_flag": {
            "expand": False
        }
    }

    if not rest:
        return flags

    tokens = shlex.split(rest)
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token == "--expand":
            flags["expand_flag"]["expand"] = True
            i += 1
            continue

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

        raise SyntaxError(f"Unknown flag: {token}")

    return flags

