# pydbms/engine/engine_base.py

'''
Common engine base class for pydbms.
All database engines (MySQL, PostgreSQL, etc.) should inherit from EngineBase.
Provides standardized output/error formatting for consistent UX.
'''

from abc import ABC, abstractmethod
from ..main.runtime import Print


class EngineBase(ABC):
    """
    Abstract base class for all database engines.

    Subclasses must implement:
        - engine_name (property)
        - connect(config)
        - execute(query, ...)
        - close()
    """

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Return the engine identifier, e.g. 'mysql', 'postgres'."""
        ...

    @abstractmethod
    def connect(self, config: dict) -> tuple:
        """Connect to the database. Return (connection, cursor) or raise."""
        ...

    @abstractmethod
    def execute(self, query: str, **kwargs):
        """Execute a query against the database."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        ...

    # ── Standardized output helpers ──────────────────────────────────

    def error(self, msg: str, *, slow_type: bool = False) -> None:
        """Print an error message: '<engine_name> error> <msg>'"""
        Print(f"{self.engine_name} error> {msg}\n", "RED", slow_type=slow_type)

    def warning(self, msg: str, *, slow_type: bool = False) -> None:
        """Print a warning message: '<engine_name> warning> <msg>'"""
        Print(f"{self.engine_name} warning> {msg}\n", "YELLOW", slow_type=slow_type)

    def info(self, msg: str, color: str = "GREEN", *, slow_type: bool = True) -> None:
        """Print an informational message."""
        Print(f"{msg}\n", color, slow_type=slow_type)


# ── Module-level helpers for pydbms-internal errors ──────────────────

def pydbms_error(msg: str, *, slow_type: bool = False) -> None:
    """Print a pydbms error: 'pydbms error> <msg>'"""
    Print(f"pydbms error> {msg}\n", "RED", slow_type=slow_type)


def pydbms_warning(msg: str, *, slow_type: bool = False) -> None:
    """Print a pydbms warning: 'pydbms warning> <msg>'"""
    Print(f"pydbms warning> {msg}\n", "YELLOW", slow_type=slow_type)


def pydbms_info(msg: str, color: str = "GREEN", *, slow_type: bool = True) -> None:
    """Print a pydbms informational message."""
    Print(f"{msg}\n", color, slow_type=slow_type)
