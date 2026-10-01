# Team assignments

Work on one Git branch per member. Run the starter script first, then improve the analysis and add a short `findings.md` in your output folder.

## Member 1: Data quality and donor profile

**Learning goals:** Explain table grain, test keys, find missing values, and reconcile joins.  
**Estimated time:** 3 hours.

### Steps

1. Run `python analyses/member_1_data_quality.py`.
2. Inventory all tables, keys, and row counts.
3. Investigate every issue reported by the validator.
4. Profile donors by membership, region, source, and giving status.
5. Recommend handling without deleting raw rows.

### Deliverables

`data_quality_issues.csv`, `donor_profile.csv`, and a written issue log.

### Completion check

You can state which duplicates affect gift totals and prove the cleaned total.

## Member 2: Solicitation ROI

**Learning goals:** Calculate response, cost, net revenue, and ROI at the right grain.  
**Estimated time:** 4 hours.

### Steps

1. Run `python analyses/member_2_solicitation_roi.py`.
2. Verify revenue joins to one solicitation and cost record.
3. Compare solicitations and then channels.
4. Investigate zero-response campaigns and missing codes.
5. Write three findings and two attribution cautions.

### Deliverables

`solicitation_roi.csv`, `channel_roi.csv`, and written findings.

### Completion check

Attributed revenue never exceeds cleaned gift revenue, and every formula is documented.

## Member 3: Monthly revenue trends

**Learning goals:** Work with dates, distinguish revenue from counts, and make readable charts.  
**Estimated time:** 4 hours.

### Steps

1. Run `python analyses/member_3_revenue_trends.py`.
2. Add year-over-year and channel-month summaries.
3. Create a second chart comparing gift count with revenue.
4. Identify seasonality and unusual months.
5. Explain why a revenue spike may not mean more donors.

### Deliverables

`monthly_revenue.csv`, two PNG charts, and written interpretation.

### Completion check

Monthly revenue sums exactly to cleaned gift revenue.

## Member 4: Donor upgrade propensity

**Learning goals:** Build donor features, prevent leakage, rank prospects, and evaluate rare outcomes.  
**Estimated time:** 5–6 hours.

### Steps

1. Run `python analyses/member_4_upgrade_propensity.py`.
2. Confirm every feature uses gifts on or before December 31, 2024.
3. Explain the point score and inspect its top 25 donors.
4. Compare the $2,500 and $5,000 targets.
5. Evaluate precision among the highest-ranked donors and document ethical limitations.

### Deliverables

`upgrade_prospects.csv`, feature definitions, evaluation table, and limitations.

### Completion check

No 2025 gift amount appears in a feature, and every ranking column is explainable.

## Member 5: Large-gift attribution and dashboard inputs

**Learning goals:** Link major gifts to campaigns, preserve unattributed gifts, and design dashboard-ready tables.  
**Estimated time:** 4 hours.

### Steps

1. Run `python analyses/member_5_large_gift_attribution.py`.
2. Compare the $2,500 and $5,000 thresholds.
3. Review direct and unattributed examples.
4. Summarize major-gift revenue by channel and solicitation.
5. Sketch cost, revenue, net revenue, ROI, and major-gift visuals.

### Deliverables

`large_gift_attribution.csv`, `dashboard_inputs.csv`, a dashboard sketch, and attribution limitations.

### Completion check

Every qualifying gift appears exactly once and has an attribution classification.
