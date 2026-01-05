# pydbms/db/db_base.py

class DBConnector:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def prompt_credentials(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError
