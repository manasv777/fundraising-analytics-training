# Coordinator guide

## Suggested schedule

1. **Kickoff (45 minutes):** explain the partner questions, synthetic-data warning, folder map, and assignments.
2. **Setup lab (60 minutes):** everyone completes Lesson 1. Record Python, Git, environment, and setup-check status.
3. **Polars lab (90 minutes):** complete Lessons 2–3 together.
4. **Independent sprint:** members work on branches `member-1-data-quality` through `member-5-attribution`.
5. **Midpoint (30 minutes):** each person reports one output, one reconciliation, and one blocker.
6. **Review (60 minutes):** use the checks below before integration.
7. **Integration (90 minutes):** assemble dashboard inputs and partner questions.

## Review gates

- The script runs from the project root in the shared environment.
- Raw files are unchanged; outputs are under `outputs/`.
- Grain, keys, filters, and joins are explained.
- Gift count, unique gift count, and revenue are reconciled.
- ROI uses net revenue divided by cost.
- Propensity features stop at the cutoff date.
- Unattributed gifts remain visible.
- Findings distinguish evidence, assumptions, and limitations.

## Git lesson for the team

After Git is installed, each person sets their identity once:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Create a branch with `git switch -c member-1-data-quality`, replacing the name for the assigned role. Use `git status` before every commit. Add only files you understand, then run `git commit -m "Describe the completed analysis"`. Do not edit another person's branch.

## Metric control sheet

- Response rate: distinct responding donors / recipients.
- Cost per donor: total cost / distinct responding donors.
- Net revenue: attributed gross revenue − total outreach cost.
- ROI: net revenue / total outreach cost.
- Major gift thresholds: $2,500 and $5,000.
- Training cutoff for features: December 31, 2024.

## Real-data handoff

1. Preserve the original partner file unchanged in a restricted location.
2. Inventory files, columns, counts, dates, and identifiers.
3. Map partner fields to this training schema without overwriting original values.
4. Rerun key, null, relationship, and reconciliation checks.
5. Confirm solicitation meanings, attribution windows, and fiscal calendar.
6. Load actual outreach costs and recipient counts.
7. Recompute the analyses before changing models or charts.
8. Document every deviation from the training assumptions.

Maintain two simple logs: a decision log with date, owner, choice, and reason; and a partner-question log with question, why it matters, owner, and status.
