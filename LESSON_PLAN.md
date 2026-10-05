# Fundraising analytics: beginner lesson plan

Work through Lessons 1–3 together before splitting into assignments. Each lesson tells you what to do, what you should see, and how to check your work. The data is synthetic.

## Lesson 1: Get the project running

**Goal:** Check Git and Python, download the private project, set up Polars, and run one successful command.

**Time:** About 60–90 minutes.

**Starting point:** You already have VS Code.

### Step 1: Confirm access

Open [the private GitHub repository](https://github.com/manasv777/fundraising-analytics-training) in a browser while signed into GitHub. You should see its file list. If GitHub shows **404**, tell Manas your GitHub username so he can grant access.

### Step 2: Check Git and Python

In VS Code, choose **Terminal → New Terminal**. Type one line at a time and press Enter.

#### Windows setup

Use **Command Prompt** for these lessons. If the terminal says `PowerShell`, click the arrow beside `+` in the terminal panel, choose **Select Default Profile → Command Prompt**, and open a new terminal.

```bat
git --version
python --version
```

If `python` is not recognized, try `py -3 --version`. Use whichever command reports Python 3.11 or newer when you create the environment in Step 5.

#### macOS setup

```bash
git --version
python3 --version
```

**Expected result:** Git prints a version, and Python prints `Python 3.11` or newer. Your exact patch numbers may differ.

### Step 3: Install a missing tool

#### Install Git (if needed)

Download [Git for Windows](https://git-scm.com/download/win) or [Git for macOS](https://git-scm.com/download/mac). On macOS, `git --version` may offer to install Apple's Command Line Tools; that also works.

#### Install Python (if needed)

Download Python 3.11 or newer from [python.org](https://www.python.org/downloads/). On Windows, enable the installer option that adds Python to your path if it appears. On macOS, the Python installer or `brew install python` works.

Close and reopen VS Code after installation. Repeat Step 2. Ask Manas for help if neither command prints a version.

### Step 4: Download and open the project

In VS Code, choose **File → Open Folder** and select a parent folder where you keep school projects (for example, `Documents`). Choose **Terminal → New Terminal**. The terminal prompt should show that parent folder; this is where the project will be downloaded. Run these lines one at a time:

```bash
git clone https://github.com/manasv777/fundraising-analytics-training.git
cd fundraising-analytics-training
```

GitHub may ask you to sign in through a browser or credential manager. Follow that prompt. If access fails, return to Step 1. If `git clone` reports that `fundraising-analytics-training` already exists, do not delete it; ask Manas whether to use that copy.

In VS Code, choose **File → Open Folder** and open the new `fundraising-analytics-training` folder. Choose **Terminal → New Terminal** again. The prompt should end with `fundraising-analytics-training`. In the Explorer, you should see `README.md`, `data`, `analyses`, and `LESSON_PLAN.md`.

### Step 5: Create a virtual environment

A virtual environment called `.venv` keeps this project's packages together. Create it once on your computer. GitHub does not store it.

#### Windows setup: Command Prompt

Use `python` in the first command if it worked in Step 2. If only `py -3` worked, replace `python` in the first command with `py -3`.

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

#### macOS setup: Terminal

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

**Expected result:** After activation, the terminal prompt begins with `(.venv)`. Installation may take several minutes and should end without an error.

### Step 6: Select `.venv` in VS Code

If VS Code offers the recommended **Python**, **Pylance**, **Jupyter**, and **Ruff** extensions, accept. Otherwise, open **Extensions** on the left and install **Python** and **Jupyter** by Microsoft.

Press **Ctrl+Shift+P** on Windows or **Command+Shift+P** on macOS. Type **Python: Select Interpreter**. Choose the interpreter whose path contains this project's `.venv`. The selected interpreter appears in VS Code's status bar.

### Step 7: Run the setup check

Open a new terminal and activate `.venv` again if its name is absent from the prompt. Then run:

```bash
python -m fundraising_analytics.setup_check
```

**Expected result:** Python and Polars versions appear; Git says `found`; the tables show `donors: 3,000`, `gifts: 9,000`, `solicitations: 29`, `outreach_costs: 29`, and `website_sources: 2,474`. The final line says to continue to Lesson 2.

**Checkpoint for Manas:** Show the five counts and the final setup message before starting an assignment.

### Common fixes

| What you see | What to do |
| --- | --- |
| `python` not found on Windows | Try `py -3 --version`. If that works, use `py -3 -m venv .venv` for the first environment command. |
| `python` not found on macOS | Use `python3` to create `.venv`; after activation, use `python`. |
| PowerShell blocks `.venv\Scripts\Activate.ps1` | Use the **Command Prompt** terminal profile and run `.venv\Scripts\activate.bat`. |
| `No module named polars` or `No module named fundraising_analytics` | Activate `.venv`, repeat the two installation commands, and reselect the VS Code interpreter. |
| A CSV file is missing | From the project folder run `python -m fundraising_analytics.generate_data`, then repeat the check. Tell Manas if a file had been edited first. |
| The terminal cannot find `requirements.txt` | Open the project folder in VS Code, then create a new terminal there. |
| GitHub login or clone fails | Confirm you can see the private repository in your browser and ask Manas to check collaborator access. |

## Lesson 2: Learn the Polars basics

**Goal:** Load a CSV, inspect it, filter rows, group results, and save a summary.

**Time:** About 60–90 minutes.

**Start when:** Lesson 1's setup check succeeds.

### Step 1: Open the notebook

Open `notebooks/00_polars_first_steps.ipynb` in VS Code. At the top right, click **Select Kernel** and choose the `.venv` Python interpreter. Run cells in order with their play buttons.

**Expected result:** The first data cell shows five donor rows. Another reports `(3000, 11)`: 3,000 rows and 11 columns. If you see a package error, revisit Lesson 1, Steps 5–6.

### Step 2: Name each operation

- `pl.read_csv(...)` opens a CSV as a Polars table.
- `.head()` previews its first rows.
- `.schema` shows each column's data type.
- `.filter(...)` keeps rows that meet a rule.
- `.group_by(...).agg(...)` summarizes groups.
- `.write_csv(...)` saves a new CSV.

### Step 3: Make one new summary

In a new notebook code cell, type:

```python
from pathlib import Path
import polars as pl

root = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
donors = pl.read_csv(root / "data/raw/donors.csv", try_parse_dates=True)
counts = donors.group_by("membership_status").agg(pl.len().alias("donors"))
print(counts.sort("membership_status"))

output_dir = root / "outputs"
output_dir.mkdir(exist_ok=True)
counts.write_csv(output_dir / "lesson_2_membership_counts.csv")
```

**Expected result:** Three membership groups appear. You should also see `outputs/lesson_2_membership_counts.csv` in VS Code's Explorer. Group order can vary unless you sort.

### Practice and checkpoint

1. Count donors by `acquisition_source`.
2. Count how many donors have `email_opt_in == True`.
3. Save the acquisition summary in `outputs/lesson_2_acquisition_counts.csv`.
4. Explain what one row of each output represents.

**Checkpoint for Manas:** Show the saved acquisition CSV and explain `filter`, `group_by`, `agg`, and `write_csv` in plain language.

## Lesson 3: Join tables and check totals

**Goal:** Connect gifts to donors and prove the join did not duplicate revenue.

**Time:** About 75–105 minutes.

**Start when:** You can complete Lesson 2's practice.

### Step 1: Learn the keys

One row in `donors.csv` is one person. One unique `gift_id` in `gifts.csv` is one transaction. The dataset also has a few duplicate gift rows for practice. `gifts.donor_id` points to `donors.donor_id`; `gifts.solicitation_code` points to `solicitations.solicitation_code` when known. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for field definitions.

### Step 2: Compare totals before and after a join

In a new notebook cell, type:

```python
from fundraising_analytics.load_data import load_tables
from fundraising_analytics.metrics import deduplicate_gifts

tables = load_tables()
gifts = deduplicate_gifts(tables["gifts"])
before_rows = gifts.height
before_revenue = gifts["gift_amount"].sum()

joined = gifts.join(tables["donors"], on="donor_id", how="left", validate="m:1")
print("Rows before / after:", before_rows, joined.height)
print("Revenue before / after:", before_revenue, joined["gift_amount"].sum())
```

**Expected result:** Both row counts match; both revenue totals match. `validate="m:1"` asks Polars to confirm that each gift matches at most one donor row.

### Step 3: Investigate practice issues

Run `python analyses/member_1_data_quality.py` in the VS Code terminal. Open `outputs/member_1/data_quality_issues.csv`. Inspect `affected_rows`, then find matching raw records. Do not delete raw rows. Record what you found in your report.

**Checkpoint for Manas:** Show the before/after totals and identify at least one issue to discuss before using real data.

## Lesson 4: Complete your assigned analysis

**Goal:** Improve your starter script and write a reviewable explanation.

**Time:** About 3–6 hours.

1. Read your section of [TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md).
2. Create your branch using [the coordinator guide](COORDINATOR_GUIDE.md#branch-and-submission-steps).
3. Run your starter script and inspect the output files.
4. Add the missing analyses listed in your assignment. Keep calculations in code so they can be rerun.
5. Copy `reports/FINDINGS_TEMPLATE.md` to `reports/member_N.md`, replacing `N` with your member number. Fill every section using your own results.
6. Run `python -m pytest -q` and your script again. Ask Manas for a review if either command fails.

**Expected result:** A script that runs, local outputs, and a report with findings, checks, limits, and a partner question.

## Lesson 5: Review and integrate

**Goal:** Combine the five analyses using consistent definitions.

**Time:** One 90-minute meeting.

Each analyst shows the command they ran, the outputs they inspected, one reconciliation, one finding, and one limitation. Manas checks that all files use the same deduplication, ROI definitions, cutoff dates, and attribution rules. The team then uses campaign ROI, monthly trends, prospect rankings, and large-gift summaries to plan the dashboard.

Before switching to partner data, inventory its columns, confirm cost and recipient data, ask what each solicitation code means, and agree on attribution windows. Recompute the analyses from real data before reporting conclusions.
