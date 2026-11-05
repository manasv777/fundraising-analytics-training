"""Member 5 lesson: attribute large gifts and prepare dashboard inputs (3–4 hours)."""

import polars as pl

from fundraising_analytics.config import OUTPUT_DIR
from fundraising_analytics.load_data import load_tables
from fundraising_analytics.metrics import calculate_roi, attribute_large_gifts, deduplicate_gifts

out = OUTPUT_DIR / "member_5"
out.mkdir(parents=True, exist_ok=True)
t = load_tables()
large = attribute_large_gifts(deduplicate_gifts(t["gifts"]), t["solicitations"], 2500)
larger=attribute_large_gifts(deduplicate_gifts(t["gifts"]), t["solicitations"], 5000)
dashboard = (
    large.with_columns(pl.col("channel").fill_null("Unattributed"))
    .group_by("channel", "attribution_type")
    .agg(pl.len().alias("gift_count"), pl.col("gift_amount").sum().alias("revenue"))
    .sort("revenue", descending=True)
)
large.write_csv(out / "large_gift_attribution.csv")
dashboard.write_csv(out / "dashboard_inputs.csv")
print(f"Wrote large-gift and dashboard inputs to {out}")

larger_dashboard = (
    larger.with_columns(pl.col("channel").fill_null("Unattributed"))
    .group_by("channel", "attribution_type")
    .agg(pl.len().alias("gift_count"), pl.col("gift_amount").sum().alias("revenue"))
    .sort("revenue", descending=True)
)

larger.write_csv(out / "larger_gift_attribution.csv")
larger_dashboard.write_csv(out / "larger_dashboard_inputs.csv")
print(f"Wrote large-gift and dashboard inputs to {out}")

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

result=larger_dashboard.join(channel, on="channel",how="left")
result.write_csv(out / "large_gifts_roi.csv")