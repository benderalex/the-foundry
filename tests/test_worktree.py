from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from foundry import worktree


def test_create_worktree_removes_stale_branch_before_add(tmp_path: Path) -> None:
    root = tmp_path / "worktrees"
    base = root / "_base"
    base.mkdir(parents=True)

    calls: list[tuple[list[str], Path | None, bool]] = []

    def fake_run(cmd: list[str], cwd: Path | None = None, check: bool = True, **kwargs):
        calls.append((cmd, cwd, check))

    with patch("foundry.worktree.shell.run", side_effect=fake_run):
        path, branch = worktree.create_worktree(root, task_id=6)

    assert path == (root / "task-6").resolve()
    assert branch == "foundry/task-6"
    assert (
        ["git", "branch", "-D", "foundry/task-6"],
        base,
        False,
    ) in calls
    assert calls[-1] == (
        ["git", "worktree", "add", str(path), "-b", "foundry/task-6", "main"],
        base,
        True,
    )


def test_ensure_base_repo_syncs_configured_base_branch(tmp_path: Path) -> None:
    root = tmp_path / "worktrees"
    base = root / "_base"
    base.mkdir(parents=True)
    calls: list[tuple[list[str], Path | None]] = []

    def fake_run(cmd: list[str], cwd: Path | None = None, **kwargs):
        calls.append((cmd, cwd))

    with patch("foundry.worktree.shell.run", side_effect=fake_run):
        out = worktree.ensure_base_repo(root, "owner/sandbox", "develop")

    assert out == base
    assert calls == [
        (["git", "fetch", "origin"], base),
        (["git", "checkout", "develop"], base),
        (["git", "reset", "--hard", "origin/develop"], base),
    ]
