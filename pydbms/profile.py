# pydbms/pydbms/main/profile.py

from .dependencies import dataclass, Optional

@dataclass
class MySQLProfile:
    host: str
    user: str
    password_hash: str  # argon2 hash

# single runtime instance
PROFILE: Optional[MySQLProfile] = None
