from __future__ import annotations

from pathlib import Path

from foundry.config import load_settings


def test_load_settings_reads_base_branch(
    tmp_path: Path,
    monkeypatch,
) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("", encoding="utf-8")
    monkeypatch.setenv("SOURCE_REPO", "owner/sandbox")
    monkeypatch.setenv("TARGET_REPO", "owner/sandbox")
    monkeypatch.setenv("BASE_BRANCH", "develop")

    settings = load_settings(env_path)

    assert settings.base_branch == "develop"


def test_load_settings_defaults_base_branch_to_main(
    tmp_path: Path,
    monkeypatch,
) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("", encoding="utf-8")
    monkeypatch.setenv("SOURCE_REPO", "owner/sandbox")
    monkeypatch.setenv("TARGET_REPO", "owner/sandbox")
    monkeypatch.delenv("BASE_BRANCH", raising=False)

    settings = load_settings(env_path)

    assert settings.base_branch == "main"
