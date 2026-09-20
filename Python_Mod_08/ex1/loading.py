#!/usr/bin/env python3
import importlib
import sys
from types import ModuleType
from typing import Optional

REQUIRED_PACKAGES: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}


def load_module(name: str) -> Optional[ModuleType]:
    try:
        return importlib.import_module(name)
    except ImportError:
        return None


def get_version(module: ModuleType) -> str:
    version = getattr(module, "__version__", None)
    if isinstance(version, str):
        return version
    return "unknown"


def display_package_differences() -> None:
    print("\nPackage Management Overview:")
    print("- pip: Traditional installer using requirements.txt (flat).")
    print("- Poetry: Modern manager using pyproject.toml and lockfiles.")


def check_dependencies() -> bool:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    missing: list[str] = []
    for pkg, description in REQUIRED_PACKAGES.items():
        module = load_module(pkg)
        if module is not None:
            version = get_version(module)
            print(f"[OK] {pkg} ({version})")
            print(f"{description}")
        else:
            print(f"[FAIL] {pkg} (missing)")
            missing.append(pkg)

    if missing:
        print("\nMissing dependencies detected!")
        print("To install via pip:    pip install -r requirements.txt")
        print("To install via Poetry: poetry install")
        return False
    return True


def run_pipeline() -> None:
    np = importlib.import_module("numpy")
    pd = importlib.import_module("pandas")
    plt = importlib.import_module("matplotlib.pyplot")

    data_points = 1000
    print("\nAnalyzing Matrix data...")
    print(f"Processing {data_points} data points...")

    raw_signal = np.random.normal(loc=0.0, scale=1.0, size=data_points)
    time_series = np.cumsum(raw_signal)

    df = pd.DataFrame({"signal": raw_signal, "matrix_flow": time_series})

    print("Generating visualization...")
    plt.figure(figsize=(10, 5))
    plt.plot(df["matrix_flow"], color="#00FF00", label="Matrix Stream")
    plt.title("Matrix Signal Analysis")
    plt.xlabel("Cycle")
    plt.ylabel("Fluctuation")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    output_filename = "matrix_analysis.png"
    plt.savefig(output_filename)
    plt.close()

    print("Analysis complete!")
    print(f"Results saved to: {output_filename}")


def main() -> None:
    if not check_dependencies():
        sys.exit(1)
    display_package_differences()
    run_pipeline()


if __name__ == "__main__":
    main()
