from pathlib import Path

from fundraising_analytics.config import OUTPUT_DIR

EXPECTED = (
    "member_1/data_quality_issues.csv",
    "member_1/donor_profile.csv",
    "member_2/solicitation_roi.csv",
    "member_3/monthly_revenue.csv",
    "member_3/monthly_revenue.png",
    "member_3/monthly_gift_count.png",
    "member_4/upgrade_prospects.csv",
    "member_4/model_evaluation.csv",
    "member_5/large_gift_attribution.csv",
    "member_5/dashboard_inputs.csv",
)
missing = [name for name in EXPECTED if not (OUTPUT_DIR / name).exists()]
if missing:
    raise SystemExit(f"Missing outputs: {', '.join(missing)}")
print(f"Verified {len(EXPECTED)} expected analysis outputs in {Path(OUTPUT_DIR).name}/")
