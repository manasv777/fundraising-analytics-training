"""Member 1 lesson: inspect data quality and build a donor profile (2–3 hours)."""

import polars as pl

from fundraising_analytics.config import OUTPUT_DIR
from fundraising_analytics.load_data import load_tables
from fundraising_analytics.metrics import deduplicate_gifts
from fundraising_analytics.validate_data import validate_tables

out = OUTPUT_DIR / "member_1"
out.mkdir(parents=True, exist_ok=True)
tables = load_tables()
issues = validate_tables(tables)
gifts = deduplicate_gifts(tables["gifts"])
profile = (
    tables["donors"]
    .join(
        gifts.group_by("donor_id").agg(pl.col("gift_amount").sum().alias("total_given")),
        on="donor_id",
        how="left",
    )
    .with_columns(pl.col("total_given").fill_null(0))
    .group_by("membership_status")
    .agg(pl.len().alias("donors"), pl.col("total_given").sum().alias("revenue"))
    .sort("revenue", descending=True)
)
issues.write_csv(out / "data_quality_issues.csv")
profile.write_csv(out / "donor_profile.csv")
print(f"Wrote {issues.height} checks and {profile.height} profile rows to {out}")
