# pydbms/pydbms/profile/profile_auth.py

import sys
from typing import Optional, Tuple
import pwinput
from ..main.profile import load_profile, save_profile
from ..main.runtime import Print, console
from crypto_functions import hash_argon2, verify_argon2

def _prompt_username() -> str:
    while True:
        u = input("Enter pydbms username: ").strip()
        if u:
            return u
        Print("pydbms error> Username cannot be empty.", "RED", slow_type)
        console.print()


def _prompt_password(prompt: str = "Enter pydbms password: ") -> str:
    while True:
        p = pwinput.pwinput(prompt, mask="*").strip()
        if p:
            return p
        Print("pydbms error> Password cannot be empty.", "RED", slow_type=False)
        console.print()


def create_new_user_flow() -> Tuple[str, str]:
    Print("Create a new local pydbms user.", "CYAN", slow_type=False)
    console.print()

    username = _prompt_username()

    while True:
        password = _prompt_password("Create password: ")
        confirm = _prompt_password("Confirm password: ")
        if password != confirm:
            Print("pydbms error> Passwords do not match. Try again.", "RED", slow_type=False)
            console.print()
            continue
        break

    password_hash = hash_argon2(password)
    save_profile({"username": username, "password_hash": password_hash})

    Print(f"User created successfully: {username}", "GREEN", slow_type=False)
    console.print()
    return username, password_hash


def login_flow(profile: dict) -> Optional[str]:
    username = _prompt_username()
    password = _prompt_password()

    saved_user = profile.get("username")
    saved_hash = profile.get("password_hash")

    if username != saved_user:
        Print("pydbms error> User not found.", "RED", slow_type=False)
        console.print()
        return None

    if not verify_argon2(password, saved_hash):
        Print("pydbms error> Incorrect password.", "RED", slow_type=False)
        console.print()
        return None

    Print(f"Login successful. Welcome {username}.", "GREEN", slow_type=False)
    console.print()
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
        Print("pydbms warning> No user exists. Want to create a login first? (y/n)", "YELLOW", slow_type=False)
        console.print()
        while True:
            ans = input("> ").strip().lower()
            if ans in ("y", "yes"):
                username, _ = create_new_user_flow()
                Print(f"Login successful. Welcome {username}.", "GREEN", slow_type=False)
                console.print()
                return username
            elif ans in ("n", "no"):
                Print("pydbms warning> Bye!", "RED", slow_type=False)
                console.print()
                sys.exit()
            else:
                Print("pydbms error> Invalid choice. Enter y/n.", "RED", slow_type=False)
                console.print()

    # Case 2: user exists => show menu
    Print("Choose your option for pydbms terminal:\n", "MAGENTA", slow_type=False)
    Print("1. Login to existing user", "CYAN", slow_type=False)
    Print("2. Create a new user\n", "CYAN", slow_type=False)
    console.print()

    while True:
        choice = input("> ").strip()
        if choice == "1":
            while True:
                username = login_flow(profile)
                if username:
                    return username
                # allow retry
                Print("pydbms warning> Try again? (y/n)\n", "YELLOW", slow_type=False)
                console.print()
                ans = input("> ").strip().lower()
                if ans in ("n", "no"):
                    Print("pydbms warning> Bye!\n", "RED", slow_type=False)
                    console.print()
                    sys.exit()
        elif choice == "2":
            username, _ = create_new_user_flow()
            Print(f"Login successful. Welcome {username}.\n", "GREEN", slow_type=False)
            console.print()
            return username
        else:
            Print("pydbms error> Invalid option. Choose 1 or 2.\n", "RED", slow_type=False)
            console.print()
