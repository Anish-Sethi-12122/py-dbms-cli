# pydbms/db/db_manager.py

from .mysql import MySQLConnector
from ..engine.engine_base import pydbms_error  # Centralized error output
from typing import Any


class connect_db:
    """Registry of supported database connectors.

    Usage:
        con, cur = connect_db.driver("mysql", config)
    """

    DRIVERS: dict[str, type] = {
        "mysql": MySQLConnector,
    }

    @staticmethod
    def driver(db_type: str, config: dict) -> tuple[Any, Any]:
        """Connect to a database by engine type.

        Args:
            db_type: Engine identifier (e.g. 'mysql').
            config: Persistent config dict with connection settings.

        Returns:
            Tuple of (connection, cursor).

        Raises:
            Exception: If the engine type is not supported.
        """
        db_type = db_type.lower()

        if db_type not in connect_db.DRIVERS:
            pydbms_error(f"Unsupported DB: {db_type}")
            raise Exception(f"Unsupported DB: {db_type}")

        connector = connect_db.DRIVERS[db_type](config)
        connector.prompt_credentials()
        return connector.connect()

