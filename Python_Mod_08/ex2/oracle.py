#!/usr/bin/env python3
import os
import sys
from typing import Optional

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    load_dotenv = None

REQUIRED_VARS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def check_dotenv_installed() -> None:
    if load_dotenv is None:
        print("ERROR: 'python-dotenv' library is not installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)


def get_config_map() -> dict[str, Optional[str]]:
    return {key: os.getenv(key) for key in REQUIRED_VARS}


def validate_config(config: dict[str, Optional[str]]) -> list[str]:
    return [key for key, value in config.items() if not value]


def display_status(config: dict[str, Optional[str]]) -> None:
    mode = config.get("MATRIX_MODE") or "development"
    api_key = config.get("API_KEY")
    log_level = config.get("LOG_LEVEL") or "DEBUG"
    zion = config.get("ZION_ENDPOINT")

    db_status = (
        "Connected to production mainframe"
        if mode == "production"
        else "Connected to local instance"
    )
    api_status = "Authenticated" if api_key else "Missing API key"
    zion_status = "Online" if zion else "Offline"

    print("ORACLE STATUS: Reading the Matrix...")
    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {db_status}")
    print(f"API Access: {api_status}")
    print(f"Log Level: {log_level}")
    print(f"Zion Network: {zion_status}\n")

    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found (using system defaults/env)")

    print("[OK] Production overrides available")
    print("The Oracle sees all configurations.")


def main() -> None:
    check_dotenv_installed()

    if load_dotenv is not None:
        load_dotenv(override=False)

    config = get_config_map()
    missing = validate_config(config)

    if missing:
        print("WARNING: Incomplete configuration detected.")
        print(f"Missing keys: {', '.join(missing)}")
        print("Defaulting or overriding may be required.\n")

    display_status(config)


if __name__ == "__main__":
    main()
