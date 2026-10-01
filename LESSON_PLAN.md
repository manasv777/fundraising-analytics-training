# Beginner lesson plan

Complete Lessons 1–3 together. Lessons 4–5 happen in assigned workstreams and review sessions.

## Lesson 1: Set up your tools

**Objective:** Prepare Python, Git, and the project environment.  
**Estimated time:** 45–75 minutes.  
**You are finished when:** the setup check lists five data tables and tells you to continue to Lesson 2.

### What the tools do

- **Python** runs the analysis code.
- **Polars** is the Python package used to work with tables.
- **Git** records versions and helps teammates work separately.
- **A terminal** is a text window for giving the computer commands.
- **A virtual environment** keeps this project's packages separate from other projects.

### Check what is already installed

In VS Code, select **Terminal → New Terminal**. Type one command at a time and press Enter.

Windows setup:

```powershell
python --version
git --version
```

macOS setup:

```bash
python3 --version
git --version
```

If Python reports 3.11 or newer and Git reports a version, continue. A “command not found” message means that tool needs installation.

### Install Python

Windows: download Python from https://www.python.org/downloads/. During installation, select **Add Python to PATH**. Close and reopen VS Code, then run `python --version`.

macOS: download the macOS installer from https://www.python.org/downloads/ or install with Homebrew using `brew install python`. Close and reopen the terminal, then run `python3 --version`.

### Install Git

Windows: download Git from https://git-scm.com/download/win and accept the standard options. Reopen VS Code and run `git --version`.

macOS: run `git --version`. macOS may offer to install Command Line Tools. Accept that prompt, or download Git from https://git-scm.com/download/mac.

### Create the virtual environment

Make sure the terminal is inside the `fundraising-analytics-training` folder.

Windows setup:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

macOS setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

In VS Code, press Command/Ctrl+Shift+P, choose **Python: Select Interpreter**, and select the interpreter containing `.venv`.

### Run the first check

```bash
python -m fundraising_analytics.setup_check
```

**Expected result:** Python and Polars versions appear, Git says `found`, and the five tables show 3,000 donors, 9,000 gift rows, 29 solicitations, 29 cost rows, and about 2,400 website responses. The final line tells you to continue to Lesson 2.

### Common fixes

- `python` is not found on macOS: use `python3` for environment creation.
- PowerShell blocks activation: open Command Prompt and use `.venv\Scripts\activate.bat`, or ask the coordinator for help changing the execution policy.
- Polars is missing: confirm `(.venv)` appears at the left of the terminal, then repeat the two `pip install` commands.
- VS Code uses the wrong Python: repeat **Python: Select Interpreter** and select `.venv`.
- A CSV is missing: run `python -m fundraising_analytics.generate_data`.

**Checkpoint:** show the coordinator the final setup-check line before continuing.

## Lesson 2: Your first Polars workflow

**Objective:** Load, inspect, filter, summarize, and save a table.  
**Estimated time:** 60–90 minutes.

Open `notebooks/00_polars_first_steps.ipynb` and select the `.venv` kernel. Run cells in order.

The basic pattern is:

```python
import polars as pl
donors = pl.read_csv("data/raw/donors.csv", try_parse_dates=True)
print(donors.shape)
print(donors.schema)
active = donors.filter(pl.col("membership_status") == "Active")
summary = active.group_by("state_group").agg(pl.len().alias("active_donors"))
summary.write_csv("outputs/lesson_2_active_donors.csv")
```

Practice questions:

1. How many active, lapsed, and prospective donors are present?
2. Which acquisition source has the most donors?
3. How many donors opted into email?
4. Save one answer as a CSV under `outputs/`.

**Completion check:** you can explain what `filter`, `group_by`, `agg`, and `write_csv` do in your own words.

## Lesson 3: Join tables without changing the money

**Objective:** Understand grain, keys, joins, and reconciliation.  
**Estimated time:** 75–105 minutes.

- Grain means what one row represents. One donor row is a person; one gift row is a transaction.
- A primary key identifies a row. `donor_id` is the donor key; `gift_id` is the gift key.
- A foreign key connects tables. `gifts.donor_id` connects gifts to donors.

Before and after every join, record row count, unique gift count, and gift total. A donor can have many gifts, so joining donor attributes onto gifts is safe only when donor IDs are unique.

Run:

```bash
python analyses/member_1_data_quality.py
```

Inspect `outputs/member_1/data_quality_issues.csv`. Decide which findings are expected training issues and which would stop a real analysis.

**Completion check:** your gift total before and after a donor join is identical.

## Lesson 4: Team analysis sprint

**Objective:** Complete one workstream using shared definitions.  
**Estimated time:** 3–6 hours depending on the assignment.

Read [TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md). First run the provided script. Then make a copy on your Git branch and improve it. Write three findings, two limitations, and one question for the partner.

## Lesson 5: Review and integrate

**Objective:** Combine the five workstreams without conflicting definitions.  
**Estimated time:** 90 minutes as a team.

Each member demonstrates the command used, reconciles totals, explains one choice, and names one limitation. The coordinator checks metric definitions, cutoff dates, attribution rules, and output filenames before dashboard assembly.

Never copy a synthetic conclusion into a partner deliverable. When real data arrives, map fields, rerun validation, confirm solicitation meanings, load actual costs and recipients, and recompute everything.
