# pydbms/db/db_manager.py

from .mysql import MySQLConnector
from ..Global import Print
import sys

class connect_db:
    DRIVERS = {
        "mysql": MySQLConnector
    }

    @staticmethod
    def driver(db_type, config):
        db_type = db_type.lower()

        if db_type not in connect_db.DRIVERS:
            Print(f"Unsupported DB: {db_type}", "RED", "bold")
            sys.exit()

        connector = connect_db.DRIVERS[db_type](config)
        connector.prompt_credentials()
        return connector.connect()
