# pydbms/db/mysql.py

from ..main.dependencies import pwinput, mysql, hash_argon2
from .db_base import DBConnector
from ..main.runtime import Print
from ..main.profile import MySQLProfile
from ..main import profile

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
            
            profile.PROFILE = MySQLProfile(
                host=self.host,
                user=self.user,
                password_hash=hash_argon2(self.password)
            )
            
            return self.connection, self.cursor

        except mysql.Error:
            Print(f"❌ Incorrect Credentials entered. Try again\n\n", "RED", "bold")
            return None, None
        
        
