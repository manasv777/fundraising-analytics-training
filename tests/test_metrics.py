from datetime import date

import polars as pl

from fundraising_analytics.generate_data import generate_all


def test_metrics_reconcile_and_keep_zero_response(tmp_path) -> None:
    from fundraising_analytics.metrics import calculate_roi, deduplicate_gifts, monthly_revenue

    tables = generate_all(output_dir=tmp_path)
    clean = deduplicate_gifts(tables["gifts"])
    monthly = monthly_revenue(clean)
    roi = calculate_roi(clean, tables["solicitations"], tables["outreach_costs"])
    assert monthly["revenue"].sum() == clean["gift_amount"].sum()
    assert roi.height == tables["solicitations"].height
    assert roi.filter(pl.col("solicitation_code") == "MAG2025TEST")["gift_count"].item() == 0


def test_upgrade_features_use_only_pre_cutoff_gifts(tmp_path) -> None:
    from fundraising_analytics.metrics import build_upgrade_features

    tables = generate_all(output_dir=tmp_path)
    features = build_upgrade_features(tables["gifts"], tables["donors"], date(2024, 12, 31))
    assert features["last_gift_date"].max() <= date(2024, 12, 31)
    assert features["join_date"].max() <= date(2024, 12, 31)
    assert {"next_gift_2500_plus", "next_gift_5000_plus"} <= set(features.columns)


def test_large_gift_attribution_retains_every_major_gift(tmp_path) -> None:
    from fundraising_analytics.metrics import attribute_large_gifts, deduplicate_gifts

    tables = generate_all(output_dir=tmp_path)
    clean = deduplicate_gifts(tables["gifts"])
    result = attribute_large_gifts(clean, tables["solicitations"], threshold=2_500)
    assert result.height == clean.filter(pl.col("gift_amount") >= 2_500).height
    assert set(result["attribution_type"].unique()) <= {"Direct", "Unattributed"}
