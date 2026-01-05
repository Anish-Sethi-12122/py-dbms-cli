# pydbms/db/mysql.py

import sys
import pwinput
import mysql.connector as mysql
from .db_base import DBConnector
from ..Global import Print

class MySQLConnector(DBConnector):

    def prompt_credentials(self):
        cfg = self.config.get("mysql", {})

        host = cfg.get("host", "localhost")
        user = cfg.get("user", "root")

        Print(f"pydbms> Enter host (default {host}): ", "YELLOW")
        self.host = input().strip() or host

        Print(f"pydbms> Enter user (default {user}): ", "YELLOW")
        self.user = input().strip() or user

        self.password = pwinput.pwinput("pydbms> Enter password: ", "*")

    def connect(self) -> tuple[object, object] | tuple[None, None]:
        try:
            self.connection = mysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password
            )
            self.cursor = self.connection.cursor()

            Print("✅ Login successful.", "GREEN")
            return self.connection, self.cursor

        except mysql.Error:
            Print(f"❌ Incorrect Password entered. Try again", "RED", "bold")
            return None, None
