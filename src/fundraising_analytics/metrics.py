from datetime import date, timedelta

import polars as pl


def deduplicate_gifts(gifts: pl.DataFrame) -> pl.DataFrame:
    return gifts.unique(subset=["gift_id"], keep="first", maintain_order=True)


def calculate_roi(
    gifts: pl.DataFrame, solicitations: pl.DataFrame, costs: pl.DataFrame
) -> pl.DataFrame:
    responses = (
        gifts.filter(pl.col("solicitation_code").is_not_null())
        .group_by("solicitation_code")
        .agg(
            pl.col("donor_id").n_unique().alias("responding_donors"),
            pl.len().alias("gift_count"),
            pl.col("gift_amount").sum().alias("gross_revenue"),
            pl.col("gift_amount").mean().alias("average_gift"),
        )
    )
    return (
        solicitations.join(costs, on="solicitation_code", how="left")
        .join(responses, on="solicitation_code", how="left")
        .with_columns(
            pl.col("responding_donors").fill_null(0),
            pl.col("gift_count").fill_null(0),
            pl.col("gross_revenue").fill_null(0.0),
        )
        .with_columns(
            (pl.col("gross_revenue") - pl.col("total_cost")).alias("net_revenue"),
            (pl.col("responding_donors") / pl.col("recipient_count")).alias("response_rate"),
            pl.when(pl.col("responding_donors") > 0)
            .then(pl.col("total_cost") / pl.col("responding_donors"))
            .otherwise(None)
            .alias("cost_per_donor"),
            pl.when(pl.col("total_cost") > 0)
            .then((pl.col("gross_revenue") - pl.col("total_cost")) / pl.col("total_cost"))
            .otherwise(None)
            .alias("roi"),
        )
        .sort(["fiscal_year", "channel", "solicitation_code"])
    )


def monthly_revenue(gifts: pl.DataFrame) -> pl.DataFrame:
    return (
        gifts.with_columns(pl.col("gift_date").dt.truncate("1mo").alias("month"))
        .group_by("month")
        .agg(
            pl.col("gift_amount").sum().alias("revenue"),
            pl.len().alias("gift_count"),
            pl.col("donor_id").n_unique().alias("donor_count"),
        )
        .sort("month")
    )


def build_upgrade_features(
    gifts: pl.DataFrame, donors: pl.DataFrame, cutoff_date: date
) -> pl.DataFrame:
    gifts = deduplicate_gifts(gifts)
    pre = gifts.filter(pl.col("gift_date") <= cutoff_date)
    recent_start = cutoff_date - timedelta(days=365)
    summary = pre.group_by("donor_id").agg(
        pl.len().alias("prior_gift_count"),
        pl.col("gift_amount").sum().alias("lifetime_revenue_at_cutoff"),
        pl.col("gift_amount").max().alias("prior_max_gift"),
        pl.col("gift_date").max().alias("last_gift_date"),
        pl.col("solicitation_code").n_unique().alias("solicitation_diversity"),
        pl.col("gift_amount")
        .filter(pl.col("gift_date") > recent_start)
        .sum()
        .alias("recent_12m_revenue"),
        pl.col("gift_date")
        .filter(pl.col("gift_date") > recent_start)
        .count()
        .alias("recent_12m_frequency"),
    )
    next_gift = (
        gifts.filter(pl.col("gift_date") > cutoff_date)
        .sort(["donor_id", "gift_date"])
        .group_by("donor_id", maintain_order=True)
        .agg(pl.col("gift_amount").first().alias("next_gift_amount"))
        .with_columns(
            (pl.col("next_gift_amount") >= 2_500).cast(pl.Int8).alias("next_gift_2500_plus"),
            (pl.col("next_gift_amount") >= 5_000).cast(pl.Int8).alias("next_gift_5000_plus"),
        )
    )
    return (
        donors.join(summary, on="donor_id", how="left")
        .join(next_gift, on="donor_id", how="left")
        .with_columns(
            pl.col(
                "prior_gift_count",
                "lifetime_revenue_at_cutoff",
                "prior_max_gift",
                "solicitation_diversity",
                "recent_12m_revenue",
                "recent_12m_frequency",
            ).fill_null(0),
            pl.col("next_gift_2500_plus", "next_gift_5000_plus").fill_null(0),
        )
        .with_columns(
            (pl.lit(cutoff_date) - pl.col("last_gift_date")).dt.total_days().alias("recency_days")
        )
    )


def attribute_large_gifts(
    gifts: pl.DataFrame, solicitations: pl.DataFrame, threshold: float
) -> pl.DataFrame:
    return (
        gifts.filter(pl.col("gift_amount") >= threshold)
        .join(
            solicitations.select("solicitation_code", "channel", "campaign_name"),
            on="solicitation_code",
            how="left",
        )
        .with_columns(
            pl.when(pl.col("channel").is_not_null())
            .then(pl.lit("Direct"))
            .otherwise(pl.lit("Unattributed"))
            .alias("attribution_type")
        )
        .sort(["gift_amount", "gift_date"], descending=[True, False])
    )
