"""Member 2 lesson: calculate solicitation and channel ROI (3–4 hours)."""

import polars as pl

from fundraising_analytics.config import OUTPUT_DIR
from fundraising_analytics.load_data import load_tables
from fundraising_analytics.metrics import calculate_roi, deduplicate_gifts

out = OUTPUT_DIR / "member_2"
out.mkdir(parents=True, exist_ok=True)
t = load_tables()
roi = calculate_roi(deduplicate_gifts(t["gifts"]), t["solicitations"], t["outreach_costs"])
channel = (
    roi.group_by("channel")
    .agg(
        pl.col("recipient_count").sum(),
        pl.col("responding_donors").sum(),
        pl.col("gift_count").sum(),
        pl.col("gross_revenue").sum(),
        pl.col("total_cost").sum(),
    )
    .with_columns(
        (pl.col("gross_revenue") - pl.col("total_cost")).alias("net_revenue"),
        ((pl.col("gross_revenue") - pl.col("total_cost")) / pl.col("total_cost")).alias("roi"),
    )
)
roi.write_csv(out / "solicitation_roi.csv")
channel.write_csv(out / "channel_roi.csv")
print(f"Wrote solicitation and channel ROI tables to {out}")
