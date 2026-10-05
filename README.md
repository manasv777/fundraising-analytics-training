# Fundraising analytics practice project

BioKind Analytics will use this project to practice the analyses planned with The American Chestnut Foundation. All records are synthetic. The results are exercises, not findings about the partner.

## Start here

1. Ask Manas for access to the private GitHub repository.
2. Follow [Lesson 1](LESSON_PLAN.md#lesson-1-get-the-project-running) to check Git and Python, download the project, and run the setup check in VS Code.
3. Complete [Lesson 2](LESSON_PLAN.md#lesson-2-learn-the-polars-basics) and [Lesson 3](LESSON_PLAN.md#lesson-3-join-tables-and-check-totals).
4. Read your section of [Team assignments](TEAM_ASSIGNMENTS.md). Each starter script makes a first pass. Your assignment is to inspect and extend it.
5. Write your conclusions in a tracked file under `reports/`. Files under `outputs/` are generated locally and ignored by Git.

Manas can use the [Coordinator guide](COORDINATOR_GUIDE.md) to run the lessons and review submissions.

## Project map

| Location | Purpose |
| --- | --- |
| `data/raw/` | Five CSV tables used by Polars; 3,000 donors and 9,000 gift rows |
| `DATA_DICTIONARY.md` | What each table and field means |
| `notebooks/` | Hands-on Polars practice |
| `analyses/` | A runnable starting script for each team member |
| `src/fundraising_analytics/` | Shared loading, data checks, and calculations |
| `tests/` | Automated checks for the code and practice data |
| `reports/` | Written findings the team commits and reviews |
| `outputs/` | Locally generated CSV and chart files; not committed |
| `reference/` | Excel copy for browsing; the CSV files are the coding inputs |

## Shared definitions

- **Attributed revenue:** gifts whose solicitation code matches a campaign.
- **Net revenue:** attributed revenue minus outreach cost.
- **ROI:** net revenue divided by outreach cost. An ROI of `1.0` means one dollar of net revenue per dollar spent.
- **Response rate:** distinct donors who gave with a campaign code divided by that campaign's recipient count. This is a practice definition; website reach and direct mail recipients may need different definitions with real data.
- **Major gifts:** the exercises use $2,500 and $5,000 thresholds.

The synthetic data can be regenerated. If you accidentally change a CSV file, tell Manas before regenerating it so your data-quality observations can be reviewed.
