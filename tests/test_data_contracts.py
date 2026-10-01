from pathlib import Path

import polars as pl
import pytest


def test_project_paths_are_anchored_to_project_root() -> None:
    from fundraising_analytics.config import OUTPUT_DIR, PROJECT_ROOT, RAW_DATA_DIR, REQUIRED_FILES

    assert RAW_DATA_DIR == PROJECT_ROOT / "data" / "raw"
    assert OUTPUT_DIR == PROJECT_ROOT / "outputs"
    assert REQUIRED_FILES == (
        "donors.csv",
        "gifts.csv",
        "solicitations.csv",
        "outreach_costs.csv",
        "website_sources.csv",
    )


def test_missing_files_name_file_and_generator(tmp_path: Path) -> None:
    from fundraising_analytics.load_data import load_tables

    with pytest.raises(FileNotFoundError, match=r"donors\.csv.*generate_data"):
        load_tables(tmp_path)


def test_validation_reports_expected_training_issues(
    generated_tables: dict[str, pl.DataFrame],
) -> None:
    from fundraising_analytics.validate_data import validate_tables

    issues = validate_tables(generated_tables)
    checks = set(issues["check_name"].to_list())
    assert "duplicate_gift_id" in checks
    assert "unknown_solicitation_code" in checks
    assert (
        issues.filter(pl.col("check_name") == "cost_components_do_not_reconcile")[
            "affected_rows"
        ].sum()
        == 0
    )


@pytest.fixture
def generated_tables(tmp_path: Path) -> dict[str, pl.DataFrame]:
    from fundraising_analytics.generate_data import generate_all

    return generate_all(output_dir=tmp_path)
