from pathlib import Path

import polars as pl

from .config import RAW_DATA_DIR, REQUIRED_FILES


def load_tables(data_dir: Path = RAW_DATA_DIR) -> dict[str, pl.DataFrame]:
    missing = [name for name in REQUIRED_FILES if not (data_dir / name).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing required data file(s): {', '.join(missing)}. "
            "Run: python -m fundraising_analytics.generate_data"
        )
    return {
        Path(name).stem: pl.read_csv(data_dir / name, try_parse_dates=True)
        for name in REQUIRED_FILES
    }
