import platform
import shutil

import polars as pl

from .load_data import load_tables


def main() -> None:
    print(f"Python: {platform.python_version()}")
    print(f"Polars: {pl.__version__}")
    print(f"Git: {'found' if shutil.which('git') else 'not found'}")
    tables = load_tables()
    for name, frame in tables.items():
        print(f"{name}: {frame.height:,} rows")
    print("Setup check complete. Continue to Lesson 2: Your first Polars workflow.")


if __name__ == "__main__":
    main()
