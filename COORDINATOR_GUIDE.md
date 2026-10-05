# Coordinator guide for Manas

## Suggested teaching sequence

| Session | Time | What everyone does | Evidence to collect |
| --- | --- | --- | --- |
| Kickoff | 30 min | Explain the nonprofit question, synthetic data, and five roles | Each person knows their role |
| Setup lab | 60–90 min | Follow Lesson 1 in VS Code | Screenshot or copied setup-check counts |
| Polars lab | 90 min | Complete Lessons 2–3 | Saved practice CSV and matching join totals |
| Independent work | 3–6 hours | Improve assigned script and write report | Branch and local outputs |
| Midpoint | 30 min | Share one finding, one check, one blocker | Updated issue list |
| Review | 60 min | Review code and reports | Approved pull requests |
| Integration | 90 min | Agree on dashboard story and partner questions | Combined outline |

Before the setup lab, add each teammate's GitHub username as a collaborator to the private repository. Ask them to accept the invitation and confirm they can see the file list. Assign one owner per workstream.

## Branch and submission steps

Demonstrate this once with a small practice edit. Each teammate runs these commands from the project folder after activating `.venv`. Member 2 is the example; replace `2` and the branch label for another role.

```bash
git switch -c member-2-solicitation-roi
git status
python analyses/member_2_solicitation_roi.py
python -m pytest -q
git add analyses/member_2_solicitation_roi.py reports/member_2.md
git commit -m "Add solicitation ROI findings"
git push -u origin member-2-solicitation-roi
```

Use VS Code's Explorer to copy `reports/FINDINGS_TEMPLATE.md` to `reports/member_2.md` before `git add`. Git may ask for a name and email before the first commit. Teammates should run `git config user.name "Their Name"` and `git config user.email "their-email@example.com"` in this project, using their real values.

After pushing, open the repository on GitHub and click **Compare & pull request** for that branch. Name the request for the workstream and summarize what changed. Manas reviews it before merging. The `outputs/` directory is intentionally ignored, so do not tell teammates to add generated CSVs or PNGs to Git; their script and report must explain how to reproduce and inspect them.

If teammates work on the same branch by mistake, pause and separate the changes before merging. Do not use `git push --force` in the teaching workflow.

## Review each submission

1. Re-run `python -m pytest -q` and the member's script on the branch.
2. Open the reported output files locally. Do the columns and row counts match the report?
3. Ask the member to explain the grain, join keys, filters, and one formula.
4. Compare raw and cleaned gift totals. Confirm no join multiplied gifts or costs.
5. Check that missing and legacy solicitation codes remain visible as unassigned.
6. For ROI, confirm `net_revenue = gross_revenue - total_cost` and `roi = net_revenue / total_cost`.
7. For propensity, confirm the feature cutoff precedes the target year and compare precision with target prevalence.
8. Require three findings, two limitations, and one concrete question for the partner.

## Shared decisions to lock before integration

- Use one gift per `gift_id` after reviewing duplicates.
- Treat a matching solicitation code as **direct** attribution. Leave unmatched and missing codes unassigned.
- Report outreach cost, attributed revenue, net revenue, and ROI at the same campaign or channel grain.
- Use the $2,500 and $5,000 major-gift thresholds.
- Describe website self-reports as donor answers, not causal proof.
- Label all training charts and reports as synthetic practice.

## When partner data arrives

1. Preserve the original file in a restricted location and leave it unchanged.
2. Inventory fields, counts, dates, identifiers, and missing values.
3. Map partner fields to this project's table structure without overwriting source values.
4. Check donor and gift keys, duplicate records, relationships, dates, and totals.
5. Ask the partner what each solicitation code means and what attribution window to use.
6. Obtain outreach cost and recipient counts by campaign and confirm what `recipient_count` means for website outreach.
7. Recompute analyses using real data and compare numbers with the partner's own reports.
8. Document all changes from the training assumptions before sharing conclusions.

Keep a decision log with **date, owner, choice, reason**, and a partner-question log with **question, why it matters, owner, status**.
