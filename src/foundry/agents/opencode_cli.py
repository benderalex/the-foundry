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


class OpencodeCliAgent:
    """Backend shelling out to the `opencode` CLI.

    Bound to one stage at construction time. `opencode run --format json`
    emits NDJSON events; resume uses `--session <id>` on subsequent calls.
    Provider auth is supplied via env (e.g. `OPENROUTER_API_KEY`).
    """

    name = "opencode_cli"

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
            message = build_fresh_prompt(self.stage, task, input)
        else:
            message = input

        cmd: list[str] = [
            "opencode", "run",
            "--format", "json",
            "--dir", str(worktree),
        ]
        if self._settings.model:
            cmd += ["-m", self._settings.model]
        if resume_id:
            cmd += ["--session", resume_id]
        cmd.append(message)

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
            sid = event.get("sessionID") or (event.get("part") or {}).get("sessionID")
            if sid:
                return str(sid)
        return None

    @staticmethod
    def _extract_final_text(events: list[dict]) -> str:
        """Concatenate all assistant text chunks in order.

        opencode emits each text block as its own `type:"text"` event with the
        full chunk in `part.text`; the final response is the concatenation.
        """
        chunks: list[str] = []
        for event in events:
            if event.get("type") != "text":
                continue
            part = event.get("part") or {}
            text = part.get("text")
            if text:
                chunks.append(str(text))
        return "".join(chunks)
