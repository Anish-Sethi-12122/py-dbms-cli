# pydbms/pydbms/main/profile.py

from dataclasses import dataclass
from typing import Optional
import json
import os
from .pydbms_path import pydbms_path

PROFILE_FILE = pydbms_path("profile.json")


class pydbmsProfile:
    @dataclass
    class Local:
        username: str
        password_hash: str  # argon2 hash

    @dataclass
    class MySQL:
        host: str
        user: str
        password_hash: str  # argon2 hash
        engine_type: str = "mysql"

def load_profile() -> dict:
    try:
        if not os.path.exists(PROFILE_FILE):
            return {}
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return {}
            data = json.loads(raw)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_profile(data: dict) -> None:
    os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# single runtime instance (optional)
PROFILE: Optional[pydbmsProfile.Local] = None
