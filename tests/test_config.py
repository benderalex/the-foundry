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


def test_auto_create_pr_defaults_to_true(
    tmp_path: Path,
    monkeypatch,
) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("", encoding="utf-8")
    monkeypatch.setenv("SOURCE_REPO", "owner/sandbox")
    monkeypatch.setenv("TARGET_REPO", "owner/sandbox")
    monkeypatch.delenv("AUTO_CREATE_PR", raising=False)

    settings = load_settings(env_path)

    assert settings.auto_create_pr is True


def test_auto_create_pr_false_from_env(
    tmp_path: Path,
    monkeypatch,
) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("", encoding="utf-8")
    monkeypatch.setenv("SOURCE_REPO", "owner/sandbox")
    monkeypatch.setenv("TARGET_REPO", "owner/sandbox")

    for value in ("false", "0", "no", "False", "NO"):
        monkeypatch.setenv("AUTO_CREATE_PR", value)
        settings = load_settings(env_path)
        assert settings.auto_create_pr is False, f"expected False for AUTO_CREATE_PR={value!r}"


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
