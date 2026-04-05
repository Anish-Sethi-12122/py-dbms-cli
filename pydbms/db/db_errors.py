# pydbms/db/db_errors.py
# Centralized DB-engine-specific error/warning/info output helpers.
# Parent class DBErrorHandler provides the standard print format.
# Each supported DB engine (MySQL, PostgreSQL, etc.) subclasses with
# its own engine_name so all output consistently reads "<engine> error> ...".

from ..main.runtime import Print


class DBErrorHandler:
    """Parent class for all DB-engine-specific terminal output.

    Subclass this and set `engine_name` to get consistent
    "<engine> error> ..." / "<engine> warning> ..." formatting
    across all database backends.

    Usage:
        class MySQLErrors(DBErrorHandler):
            engine_name = "mysql"

        MySQLErrors.error("Connection refused")
        # prints: "mysql error> Connection refused"
    """

    engine_name: str = "db"

    @classmethod
    def error(cls, msg: str, *, slow_type: bool = False) -> None:
        """Print a DB error: '<engine> error> <msg>' in RED."""
        Print(f"{cls.engine_name} error> {msg}\n", "RED", slow_type=slow_type)

    @classmethod
    def warning(cls, msg: str, *, slow_type: bool = False) -> None:
        """Print a DB warning: '<engine> warning> <msg>' in YELLOW."""
        Print(f"{cls.engine_name} warning> {msg}\n", "YELLOW", slow_type=slow_type)

    @classmethod
    def info(cls, msg: str, color: str = "GREEN", *, slow_type: bool = True) -> None:
        """Print a DB informational message in GREEN (with typing effect)."""
        Print(f"{msg}\n", color, slow_type=slow_type)


class MySQLErrors(DBErrorHandler):
    """MySQL-specific error/warning/info output.

    All calls will be prefixed with 'mysql error>' or 'mysql warning>'.
    """

    engine_name: str = "mysql"
