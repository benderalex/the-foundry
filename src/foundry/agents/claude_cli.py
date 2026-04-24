from __future__ import annotations

from pathlib import Path

from .base import (
    AgentResult,
    AgentStage,
    AgentTask,
    build_fresh_prompt,
    first_line,
    run_cli_jsonl,
)
from .config import AgentSettings


class ClaudeCliAgent:
    """Backend shelling out to the `claude` CLI (Anthropic subscription OAuth).

    Bound to one stage at construction time. Session state is private,
    keyed by task id: first call for a given task renders the prompt
    template from `prompts/<stage>.md`; subsequent calls pass
    `--resume <id>` with just `input`.
    """

    name = "claude_cli"

    def __init__(self, settings: AgentSettings) -> None:
        self._settings = settings
        self.stage: AgentStage = settings.stage
        self._sessions: dict[int, str] = {}

    def apply(
        self,
        task: AgentTask,
        worktree: Path,
        input: str = "",
    ) -> AgentResult:
        resume_id = self.get_session_id(task)
        if resume_id is None:
            prompt = build_fresh_prompt(self.stage, task, input)
        else:
            prompt = input

        cmd: list[str] = [
            "claude",
            "-p",
            prompt,
            "--output-format",
            "stream-json",
            "--verbose",
            "--permission-mode",
            "acceptEdits",
            "--max-turns",
            str(self._settings.max_turns),
        ]
        if self._settings.model:
            cmd += ["--model", self._settings.model]
        if resume_id:
            cmd += ["--resume", resume_id]

        events = run_cli_jsonl(cmd, cwd=worktree, timeout_sec=self._settings.timeout_sec)

        new_session_id = self._extract_session_id(events)
        if new_session_id:
            self._sessions[task.id] = new_session_id

        response = self._extract_final_text(events)
        return AgentResult(
            stage=self.stage,
            response=response,
            result=first_line(response),
        )

    def get_session_id(self, task: AgentTask) -> str | None:
        return self._sessions.get(task.id)

    @staticmethod
    def _extract_session_id(events: list[dict]) -> str | None:
        for event in events:
            if event.get("type") == "system" and event.get("session_id"):
                return str(event["session_id"])
        return None

    @staticmethod
    def _extract_final_text(events: list[dict]) -> str:
        for event in reversed(events):
            if event.get("type") == "result" and "result" in event:
                return str(event["result"])
        for event in reversed(events):
            if event.get("type") == "assistant":
                message = event.get("message") or {}
                for block in message.get("content", []):
                    if block.get("type") == "text":
                        return str(block.get("text", ""))
        return ""
