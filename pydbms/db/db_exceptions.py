# pydbms/db/db_exceptions.py

class DatabaseError(Exception):
    pass

class ConnectionError(DatabaseError):
    pass

class QueryError(DatabaseError):
    pass