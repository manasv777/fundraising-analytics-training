# Fundraising analytics training

This project gives BioKind Analytics a safe practice version of the work planned for The American Chestnut Foundation. Every donor and gift is synthetic. Do not treat the patterns as findings about the partner.

## Start here

1. Open this folder in VS Code.
2. Follow **Lesson 1** in [LESSON_PLAN.md](LESSON_PLAN.md).
3. Complete the Polars practice before starting a team assignment.
4. Read your role in [TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md).
5. Save all generated work under `outputs/`.

The CSV files in `data/raw/` are the coding source. The Excel file in `reference/` is only for browsing.

## Project map

- `data/raw/`: five related practice tables.
- `src/fundraising_analytics/`: reusable loading, validation, metrics, and generation code.
- `analyses/`: one guided workstream per team member.
- `notebooks/`: first Polars lesson.
- `tests/`: automatic checks.
- `outputs/`: generated results.
- `data/answers/`: coordinator-only answer key.

## Important definitions

- Net revenue = attributed revenue − outreach cost.
- ROI = net revenue ÷ outreach cost.
- Response rate = distinct responding donors ÷ recipients.
- Direct attribution means the gift carries a solicitation code found in the solicitation table.

These definitions are starting assumptions. Confirm them with the partner before analyzing real data.
