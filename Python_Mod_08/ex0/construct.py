#!/usr/bin/env python3
import os
import site
import sys


def is_in_virtualenv() -> bool:
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    return hasattr(sys, "real_prefix") or sys.prefix != base_prefix


def get_site_packages_path() -> str:
    packages = site.getsitepackages()
    if isinstance(packages, list) and len(packages) > 0:
        return str(packages[0])
    return "Unknown"


def show_construct_env() -> None:
    env_path = sys.prefix
    env_name = os.path.basename(env_path)
    site_packages = get_site_packages_path()

    print("MATRIX STATUS: Welcome to the construct")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {env_name}")
    print(f"Environment Path: {env_path}\n")
    print(
        "SUCCESS: You're in an isolated environment!\n"
        "Safe to install packages without affecting\n"
        "the global system.\n"
    )
    print(f"Package installation path:\n{site_packages}")


def show_global_env() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")
    print(
        "WARNING: You're in the global environment!\n"
        "The machines can see everything you install.\n"
    )
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate")
    print("\nThen run this program again.")


def main() -> None:
    if is_in_virtualenv():
        show_construct_env()
    else:
        show_global_env()


if __name__ == "__main__":
    main()
