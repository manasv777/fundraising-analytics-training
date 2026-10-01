"""Member 4 lesson: rank donors with cutoff-safe, explainable features (4–6 hours)."""

from datetime import date

import polars as pl
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from fundraising_analytics.config import OUTPUT_DIR
from fundraising_analytics.load_data import load_tables
from fundraising_analytics.metrics import build_upgrade_features

out = OUTPUT_DIR / "member_4"
out.mkdir(parents=True, exist_ok=True)
t = load_tables()

FEATURE_COLUMNS = [
    "prior_gift_count",
    "lifetime_revenue_at_cutoff",
    "prior_max_gift",
    "recent_12m_revenue",
    "recent_12m_frequency",
    "solicitation_diversity",
    "recency_days",
    "event_attendance_count",
    "email_opt_in",
    "volunteer",
]


def features_and_one_year_targets(cutoff: date, target_year: int) -> pl.DataFrame:
    features = build_upgrade_features(t["gifts"], t["donors"], cutoff).drop(
        "next_gift_amount", "next_gift_2500_plus", "next_gift_5000_plus"
    )
    targets = (
        t["gifts"]
        .filter(pl.col("gift_date").dt.year() == target_year)
        .group_by("donor_id")
        .agg(pl.col("gift_amount").max().alias("target_year_max_gift"))
        .with_columns(
            (pl.col("target_year_max_gift") >= 2_500).cast(pl.Int8).alias("next_gift_2500_plus"),
            (pl.col("target_year_max_gift") >= 5_000).cast(pl.Int8).alias("next_gift_5000_plus"),
        )
    )
    return features.join(targets, on="donor_id", how="left").with_columns(
        pl.col("target_year_max_gift").fill_null(0),
        pl.col("next_gift_2500_plus", "next_gift_5000_plus").fill_null(0),
        pl.col("recency_days").fill_null(9999),
    )


train = features_and_one_year_targets(date(2023, 12, 31), 2024)
features = features_and_one_year_targets(date(2024, 12, 31), 2025)
ranked = features.with_columns(
    (
        (pl.col("prior_max_gift") >= 1000).cast(pl.Int8) * 3
        + (pl.col("recent_12m_frequency") >= 2).cast(pl.Int8) * 2
        + (pl.col("recent_12m_revenue") >= 1500).cast(pl.Int8) * 3
        + (pl.col("event_attendance_count") >= 2).cast(pl.Int8)
    ).alias("upgrade_score")
)

evaluation_rows = []
for threshold, target in ((2500, "next_gift_2500_plus"), (5000, "next_gift_5000_plus")):
    model = make_pipeline(
        StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000)
    )
    model.fit(train.select(FEATURE_COLUMNS).to_numpy(), train[target].to_numpy())
    probabilities = model.predict_proba(features.select(FEATURE_COLUMNS).to_numpy())[:, 1]
    ranked = ranked.with_columns(pl.Series(f"propensity_{threshold}", probabilities))
    y_true = features[target].to_numpy()
    cutoff = max(1, len(probabilities) // 10)
    top_indices = probabilities.argsort()[-cutoff:]
    evaluation_rows.append(
        {
            "threshold": threshold,
            "positive_donors": int(y_true.sum()),
            "average_precision": float(average_precision_score(y_true, probabilities)),
            "top_decile_precision": float(y_true[top_indices].mean()),
        }
    )

ranked = ranked.sort(
    ["upgrade_score", "propensity_2500", "prior_max_gift"], descending=True
).select(
    "donor_id",
    "upgrade_score",
    "propensity_2500",
    "propensity_5000",
    "prior_max_gift",
    "recent_12m_revenue",
    "recent_12m_frequency",
    "recency_days",
    "next_gift_2500_plus",
    "next_gift_5000_plus",
)
ranked.write_csv(out / "upgrade_prospects.csv")
pl.DataFrame(evaluation_rows).write_csv(out / "model_evaluation.csv")
print(f"Wrote {ranked.height} ranked donors and time-based evaluation to {out}")
