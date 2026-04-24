from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from .base import AgentStage


DEFAULT_MAX_TURNS: dict[AgentStage, int] = {
    AgentStage.PLAN: 50,
    AgentStage.IMPLEMENT: 50,
    AgentStage.VERIFY: 20,
}


@dataclass(frozen=True)
class AgentSettings:
    """Settings for a single-stage agent.

    One agent instance is bound to one stage at construction time. To run a
    full pipeline you build three separate agents with three separate
    settings — they can differ in backend, model, turn cap, and timeout.
    """

    stage: AgentStage
    backend: str = "stub"
    timeout_sec: int = 600
    max_turns: int = 30
    model: str = "haiku"

    @classmethod
    def from_env(cls, stage: AgentStage) -> AgentSettings:
        """Load settings for `stage` from environment.

        Per-stage env vars (e.g. `AGENT_PLAN_MODEL`) win over global ones
        (`AGENT_MODEL`); global wins over hard-coded defaults.
        """
        load_dotenv()
        key = stage.value.upper()
        model = os.getenv(f"AGENT_{key}_MODEL") or os.getenv("AGENT_MODEL", "haiku")
        timeout = int(
            os.getenv(f"AGENT_{key}_TIMEOUT_SEC")
            or os.getenv("AGENT_TIMEOUT_SEC", "600")
        )
        max_turns = int(
            os.getenv(f"AGENT_{key}_MAX_TURNS")
            or os.getenv("AGENT_MAX_TURNS", str(DEFAULT_MAX_TURNS[stage]))
        )
        return cls(
            stage=stage,
            backend=os.getenv(f"AGENT_{key}_BACKEND") or os.getenv("CODING_AGENT", "stub"),
            timeout_sec=timeout,
            max_turns=max_turns,
            model=model,
        )
