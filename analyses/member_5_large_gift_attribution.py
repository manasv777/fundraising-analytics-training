"""Member 5 lesson: attribute large gifts and prepare dashboard inputs (3–4 hours)."""

import polars as pl

from fundraising_analytics.config import OUTPUT_DIR
from fundraising_analytics.load_data import load_tables
from fundraising_analytics.metrics import attribute_large_gifts, deduplicate_gifts

out = OUTPUT_DIR / "member_5"
out.mkdir(parents=True, exist_ok=True)
t = load_tables()
large = attribute_large_gifts(deduplicate_gifts(t["gifts"]), t["solicitations"], 2500)
dashboard = (
    large.with_columns(pl.col("channel").fill_null("Unattributed"))
    .group_by("channel", "attribution_type")
    .agg(pl.len().alias("gift_count"), pl.col("gift_amount").sum().alias("revenue"))
    .sort("revenue", descending=True)
)
large.write_csv(out / "large_gift_attribution.csv")
dashboard.write_csv(out / "dashboard_inputs.csv")
print(f"Wrote large-gift and dashboard inputs to {out}")
