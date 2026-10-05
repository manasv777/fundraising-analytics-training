# Five team assignments

Finish Lessons 1–3 before starting your assignment. Each script already produces a **first pass** so you can inspect a working example. Your job is to improve it, answer the additional questions below, and explain your choices. Run commands from the project folder with `.venv` active. The generated `outputs/` files stay on your computer; submit your changed code and a `reports/member_N.md` file through GitHub.

Use [the findings template](reports/FINDINGS_TEMPLATE.md) for the report. In every report, include three findings, two limitations, and one question for the nonprofit partner. Show numbers and the filenames that support each finding. Never present these synthetic results as partner findings.

## Member 1: Data quality and donor profile

**Learning goals:** Identify table grain and keys, check duplicates and missing values, and reconcile a donor join.

**Estimated time:** 3 hours.

**Business question:** Can the donor and gift tables support trustworthy analysis?

### Steps

1. Run `python analyses/member_1_data_quality.py`. Open `outputs/member_1/data_quality_issues.csv` and `donor_profile.csv`.
2. Write down the grain and key for all five input tables. Count rows, unique keys, and missing values with Polars. Use `pl.col("gift_id").n_unique()` as a hint.
3. Compare raw gift rows with deduplicated gift rows and calculate the difference in revenue. The shared `deduplicate_gifts` function keeps the first row for each gift ID; inspect duplicates before relying on that rule.
4. Extend your script to summarize donors by `state_group` and `acquisition_source`. Add a giving-status column based on whether a donor has at least one cleaned gift.
5. Save your new summaries as `outputs/member_1/donor_by_region.csv` and `donor_by_source.csv`. Write an issue log in `reports/member_1.md`: issue, affected rows, impact on analysis, and recommended handling.

### Deliverables

The four CSV summaries, an issue log, and the changed Member 1 script.

### Completion check

Show the raw and cleaned gift counts, reconcile the cleaned total after joining donors, and explain why a duplicate gift ID could overstate revenue.

## Member 2: Solicitation ROI

**Learning goals:** Join gifts to campaigns and costs, calculate ROI, and explain attribution limits.

**Estimated time:** 4 hours.

**Business question:** Which coded outreach activities returned the most net revenue?

### Steps

1. Run `python analyses/member_2_solicitation_roi.py`. Open `solicitation_roi.csv` and `channel_roi.csv` in `outputs/member_2/`.
2. Trace one campaign from `solicitations.csv` to its cost row and matching gifts. Check that campaign costs appear once in the ROI table.
3. Recalculate one row by hand: `net_revenue = gross_revenue - total_cost`; `roi = net_revenue / total_cost`. Check your answer against the CSV.
4. Extend your script with a compact table that compares all four channels on attributed revenue, cost, net revenue, ROI, gift count, and recipient count. Save it as `outputs/member_2/channel_comparison.csv`.
5. Count gifts with a missing or unmatched solicitation code. Explain how excluding them changes the meaning of direct-response ROI. Do not force them into a channel.
6. Write three findings and two attribution cautions in `reports/member_2.md`. Explain that summing campaign-level responding donors counts the same person more than once if they answered two campaigns.

### Deliverables

`solicitation_roi.csv`, `channel_roi.csv`, `channel_comparison.csv`, report, and changed script.

### Completion check

The sum of campaign-attributed revenue is no greater than cleaned gift revenue. Your report defines the formula and states what unassigned gifts were excluded.

## Member 3: Monthly revenue trends

**Learning goals:** Aggregate dates, reconcile yearly totals, and explain two different trends.

**Estimated time:** 4 hours.

**Business question:** When do gifts and revenue arrive during the year?

### Steps

1. Run `python analyses/member_3_revenue_trends.py`. Open `monthly_revenue.csv`, `monthly_revenue.png`, and `monthly_gift_count.png` in `outputs/member_3/`.
2. Add year and month-number columns using `pl.col("gift_date").dt.year()` and `.dt.month()`. Aggregate revenue and gift count by year and month.
3. Save the comparison as `outputs/member_3/year_over_year_monthly.csv` with one row per year/month. Add a channel-by-month table as `channel_monthly.csv`; join gift codes to solicitation channels and keep an `Unattributed` category.
4. Compare the revenue and gift-count charts. Identify a month where the two stories differ. Check whether a few large gifts explain the gap.
5. In `reports/member_3.md`, describe the yearly pattern, one unusual month, one reconciliation, and chart limitations.

### Deliverables

Three CSV tables, two PNG charts, report, and changed script.

### Completion check

The sum of all monthly revenue equals cleaned gift revenue. Each month is in calendar order and each chart has a title and labeled axes.

## Member 4: Donor upgrade propensity

**Learning goals:** Build features only from prior information, understand rare outcomes, and evaluate an explainable ranking.

**Estimated time:** 5–6 hours.

**Business question:** Which donors might merit a conversation about a $2,500+ or $5,000+ gift?

### Steps

1. Run `python analyses/member_4_upgrade_propensity.py`. Open `upgrade_prospects.csv` and `model_evaluation.csv` in `outputs/member_4/`.
2. Read `FEATURE_COLUMNS` in the script. Verify that the 2024 training features use gifts through December 31, 2023 and the 2025 evaluation features use gifts through December 31, 2024. Targets are the donor's **largest gift in the following year**, not their immediate next transaction.
3. Explain each point-score rule. Inspect the top 25 donors. The `propensity_2500` and `propensity_5000` columns are model scores, not promises or verified probabilities for real donors. The `following_year_*` columns are known outcomes included only to evaluate this synthetic exercise; you would not know them when ranking current real prospects.
4. Compare each target's prevalence (`positive_donors / evaluated_donors`) with `average_precision` and `top_decile_precision`. Add the prevalence and evaluated-donor count to `model_evaluation.csv` in your script.
5. Check whether a model trained on 2024 outcomes performs on 2025 outcomes better than simply ranking by prior maximum gift. Document the comparison in your report. A modest result is still useful to learn from.
6. Exclude fields whose value might have been updated after the cutoff unless a historical snapshot exists. Write a one-page feature list, leakage check, and prioritization limits in `reports/member_4.md`.

### Deliverables

Prospect ranking, evaluation table, feature/leakage explanation, report, and changed script.

### Completion check

No 2025 gift amount is used as a 2024 feature. Your report names the target period, comparison baseline, and the number of positive donors at both thresholds.

## Member 5: Large-gift attribution and dashboard inputs

**Learning goals:** Classify large gifts, preserve unknown attribution, and combine campaign return with major-gift context.

**Estimated time:** 4 hours.

**Business question:** Which solicitations can be linked directly to $2,500+ and $5,000+ gifts?

### Steps

1. Run `python analyses/member_5_large_gift_attribution.py`. Open `large_gift_attribution.csv` and `dashboard_inputs.csv` in `outputs/member_5/`.
2. Filter `large_gift_attribution.csv` again at $5,000. Count and sum both thresholds, then reconcile them to the cleaned gifts table.
3. Group direct-attributed major gifts by solicitation code and channel. Save `outputs/member_5/major_gifts_by_solicitation.csv`.
4. Join the Member 2 ROI result (or recalculate it with `calculate_roi`) to your channel-level major-gift summary. Save `dashboard_channel_summary.csv` with outreach cost, attributed revenue, net revenue, ROI, and major-gift revenue side by side.
5. Draw a simple dashboard sketch in `reports/member_5.md`: which chart answers the cost-versus-revenue question, which chart shows monthly trends, and where unattributed gifts appear.
6. Explain one direct match and one unattributed gift. Do not infer a cause from the website self-report field without an agreed attribution rule.

### Deliverables

Gift-level attribution, solicitation summary, channel dashboard table, dashboard sketch, report, and changed script.

### Completion check

Every cleaned gift at or above $2,500 appears once in the gift-level file. Direct, unattributed, and any proposed inferred categories are defined, and no money disappears from the threshold reconciliation.
