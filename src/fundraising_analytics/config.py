from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
REQUIRED_FILES = (
    "donors.csv",
    "gifts.csv",
    "solicitations.csv",
    "outreach_costs.csv",
    "website_sources.csv",
)
