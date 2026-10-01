from datetime import date

import polars as pl


def test_generation_is_reproducible_and_sized(tmp_path) -> None:
    from fundraising_analytics.generate_data import generate_all

    first = generate_all(output_dir=tmp_path / "a")
    second = generate_all(output_dir=tmp_path / "b")
    assert all(first[name].equals(second[name]) for name in first)
    assert first["donors"].height == 3_000
    assert 8_500 <= first["gifts"].height <= 9_500
    assert first["gifts"]["gift_date"].min() >= date(2022, 1, 1)
    assert first["gifts"]["gift_date"].max() <= date(2025, 12, 31)


def test_generation_has_major_gifts_channels_and_issues(tmp_path) -> None:
    from fundraising_analytics.generate_data import generate_all

    tables = generate_all(output_dir=tmp_path)
    gifts = tables["gifts"]
    assert gifts.filter(pl.col("gift_amount") >= 2_500).height >= 100
    assert gifts.filter(pl.col("gift_amount") >= 5_000).height >= 40
    assert {"Renewal", "Year-end letter", "Magazine", "Website"} <= set(
        tables["solicitations"]["channel"].to_list()
    )
    assert gifts["gift_id"].n_unique() < gifts.height
    assert gifts["solicitation_code"].null_count() > 0
