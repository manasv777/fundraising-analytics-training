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


def test_gifts_follow_donor_join_and_matched_campaign_send_dates(tmp_path) -> None:
    from fundraising_analytics.generate_data import generate_all

    tables = generate_all(output_dir=tmp_path)
    gifts = tables["gifts"].unique("gift_id")
    joined = gifts.join(
        tables["donors"].select("donor_id", "join_date"), on="donor_id", how="left"
    ).join(
        tables["solicitations"].select("solicitation_code", "send_date"),
        on="solicitation_code",
        how="left",
    )
    assert joined.filter(pl.col("gift_date") < pl.col("join_date")).height == 0
    assert joined.filter(pl.col("gift_date") < pl.col("send_date")).height == 0


def test_recurring_flag_matches_gift_type(tmp_path) -> None:
    from fundraising_analytics.generate_data import generate_all

    gifts = generate_all(output_dir=tmp_path)["gifts"]
    inconsistent = gifts.filter(
        (pl.col("gift_type") == "Recurring") != pl.col("recurring_gift")
    )
    assert inconsistent.height == 0


def test_website_gifts_use_online_payment_methods(tmp_path) -> None:
    from fundraising_analytics.generate_data import generate_all

    gifts = generate_all(output_dir=tmp_path)["gifts"]
    unexpected = gifts.filter(pl.col("online") & ~pl.col("payment_method").is_in(["Card", "ACH"]))
    assert unexpected.height == 0
