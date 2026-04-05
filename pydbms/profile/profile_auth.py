# pydbms/pydbms/profile/profile_auth.py
# Local profile authentication — login, user creation, Argon2 hashing.

import sys
from typing import Optional, Tuple
import pwinput
from ..main.profile import load_profile, save_profile
from ..main.runtime import Print, PrintNewline
from ..engine.engine_base import pydbms_error, pydbms_warning  # Centralized UX helpers
from crypto_functions import hash_argon2, verify_argon2

def _prompt_username() -> str:
    while True:
        u = input("Enter pydbms username: ").strip()
        if u:
            return u
        pydbms_error("Username cannot be empty.", slow_type=False)

def _prompt_password(prompt: str = "Enter pydbms password: ") -> str:
    while True:
        p = pwinput.pwinput(prompt, mask="*").strip()
        if p:
            return p
        pydbms_error("Password cannot be empty.", slow_type=False)


def create_new_user_flow() -> Tuple[str, str]:
    Print("Create a new local pydbms user.\n", "CYAN", slow_type=False)

    username = _prompt_username()

    while True:
        password = _prompt_password("Create password: ")
        confirm = _prompt_password("Confirm password: ")
        if password != confirm:
            pydbms_error("Passwords do not match. Try again.", slow_type=False)
            continue
        break

    password_hash = hash_argon2(password)
    save_profile({"username": username, "password_hash": password_hash})

    Print(f"User created successfully: {username}\n", "GREEN", slow_type=False)
    return username, password_hash


def login_flow(profile: dict) -> Optional[str]:
    username = _prompt_username()
    password = _prompt_password()

    saved_user = profile.get("username")
    saved_hash = profile.get("password_hash")

    if username != saved_user:
        pydbms_error("User not found.", slow_type=False)
        return None

    if not verify_argon2(password, saved_hash):
        pydbms_error("Incorrect password.", slow_type=False)
        return None

    Print(f"Login successful. Welcome {username}.\n", "GREEN", slow_type=False)
    return username


def ensure_local_profile_login() -> str:
    """
    v4.0.0 behavior:
    - if profile exists: show menu (login / create new user)
    - if profile missing/corrupted: ask to create new user else exit
    """
    profile = load_profile()

    # Case 1: no usable user exists
    if not profile or not isinstance(profile, dict) or not profile.get("username") or not profile.get("password_hash"):
        pydbms_warning("No user exists. Want to create a login first? (y/n)", slow_type=False)
        while True:
            ans = input("> ").strip().lower()
            if ans in ("y", "yes"):
                username, _ = create_new_user_flow()
                Print(f"Login successful. Welcome {username}.\n", "GREEN", slow_type=False)
                return username
            elif ans in ("n", "no"):
                pydbms_warning("Bye!", slow_type=False)
                sys.exit()
            else:
                pydbms_error("Invalid choice. Enter y/n.", slow_type=False)

    # Case 2: user exists => show menu
    Print("Choose your option for pydbms terminal:\n", "MAGENTA", slow_type=False)
    Print("1. Login to existing user\n", "CYAN", slow_type=False)
    Print("2. Create a new user\n", "CYAN", slow_type=False)
    PrintNewline()

    while True:
        choice = input("> ").strip()
        if choice == "1":
            while True:
                username = login_flow(profile)
                if username:
                    return username
                # allow retry
                pydbms_warning("Try again? (y/n)", slow_type=False)
                ans = input("> ").strip().lower()
                if ans in ("n", "no"):
                    pydbms_warning("Bye!", slow_type=False)
                    sys.exit()
        elif choice == "2":
            username, _ = create_new_user_flow()
            Print(f"Login successful. Welcome {username}.\n", "GREEN", slow_type=False)
            return username
        else:
            pydbms_error("Invalid option. Choose 1 or 2.", slow_type=False)
