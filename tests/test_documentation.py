import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_lesson_plan_has_beginner_setup_contract() -> None:
    text = (ROOT / "LESSON_PLAN.md").read_text()
    for item in (
        "Windows setup",
        "macOS setup",
        "Install Python",
        "Install Git",
        "python --version",
        "python3 --version",
        "git --version",
        "fundraising_analytics.setup_check",
        "Expected result",
        "Common fixes",
    ):
        assert item in text


def test_team_assignments_scaffold_all_five_members() -> None:
    text = (ROOT / "TEAM_ASSIGNMENTS.md").read_text()
    for member in range(1, 6):
        assert f"## Member {member}:" in text
    for label in ("Learning goals", "Estimated time", "Steps", "Deliverables", "Completion check"):
        assert text.count(label) >= 5


def test_vscode_and_notebook_files_are_valid_json() -> None:
    for relative in (
        ".vscode/extensions.json",
        ".vscode/settings.json",
        ".vscode/tasks.json",
        "notebooks/00_polars_first_steps.ipynb",
    ):
        content = json.loads((ROOT / relative).read_text())
        if relative.endswith(".ipynb"):
            assert all(cell.get("id") for cell in content["cells"])


def test_vscode_uses_platform_discovered_environment() -> None:
    settings = json.loads((ROOT / ".vscode/settings.json").read_text())
    assert "python.defaultInterpreterPath" not in settings
