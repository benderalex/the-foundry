from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from foundry.config import Settings
from foundry.models import Task
from foundry.shell import Result
from foundry.stages import pr
from foundry.stages.pr import MAX_FILES_PER_PR, _sanity_check_changes


def test_sanity_check_accepts_small_clean_change() -> None:
    lines = [" M src/foundry/pipeline.py", "?? README.md"]

    _sanity_check_changes(lines)


def test_sanity_check_rejects_too_many_files() -> None:
    lines = [f" M file_{i}.py" for i in range(MAX_FILES_PER_PR + 1)]

    with pytest.raises(RuntimeError, match="sandbox escape"):
        _sanity_check_changes(lines)


def test_sanity_check_rejects_pycache_paths() -> None:
    lines = [" M src/foundry/__pycache__/pipeline.cpython-311.pyc"]

    with pytest.raises(RuntimeError, match="forbidden paths"):
        _sanity_check_changes(lines)


def test_sanity_check_rejects_venv_paths() -> None:
    lines = [" M .venv/bin/activate"]

    with pytest.raises(RuntimeError, match="forbidden paths"):
        _sanity_check_changes(lines)


def test_sanity_check_rejects_ds_store() -> None:
    lines = ["?? .DS_Store"]

    with pytest.raises(RuntimeError, match="forbidden paths"):
        _sanity_check_changes(lines)


def test_sanity_check_allows_env_example() -> None:
    """`.env.example` must not be caught by a forbidden substring — it's legitimate."""
    lines = [" M .env.example"]

    _sanity_check_changes(lines)


def test_pr_create_uses_configured_base_branch(tmp_path: Path) -> None:
    settings = Settings(
        source_repo="owner/sandbox",
        target_repo="owner/sandbox",
        issue_label="agent-task",
        worktree_root=tmp_path / "worktrees",
        db_path=tmp_path / "foundry.sqlite",
        poll_interval_seconds=30,
        base_branch="develop",
    )
    task = Task(
        repo="owner/sandbox",
        issue_number=42,
        issue_title="do the thing",
        issue_body="",
    )
    commands: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs) -> Result:
        commands.append(cmd)
        return Result(
            returncode=0,
            stdout="https://github.com/owner/sandbox/pull/1\n",
            stderr="",
        )

    with patch(
        "foundry.stages.pr.commit_and_push_changes",
        return_value={"touched_files": ["README.md"], "files_changed": 1},
    ), patch("foundry.stages.pr.shell.run", side_effect=fake_run):
        pr.run(task, tmp_path, "foundry/task-42", settings)

    pr_create = next(cmd for cmd in commands if cmd[:3] == ["gh", "pr", "create"])
    base_index = pr_create.index("--base")
    assert pr_create[base_index + 1] == "develop"
