// AskAgentComposer — UI-only stub for PR6.
// The actual POST endpoint is deliberately out of scope (see
// docs/specs/observability-ui-plan.md, PR6 → "Не делаем: POST /ask").

import type { JSX } from "react";
import { useState } from "react";
import { Lightbulb } from "lucide-react";

import type { AgentInfo } from "../api";

interface Props {
  agent?: AgentInfo | null;
  stageLabel: string;
}

export default function AskAgentComposer({ agent, stageLabel }: Props): JSX.Element {
  const [value, setValue] = useState("");
  const agentName = agent?.name ?? "агента";

  return (
    <div
      style={{
        padding: "12px 14px",
        borderTop: "1px solid var(--border)",
        background: "var(--bg-1)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          marginBottom: 8,
        }}
      >
        <Lightbulb
          className="ico-sm"
          style={{ color: "var(--highlight)" }}
        />
        <span
          style={{
            fontSize: 11,
            letterSpacing: ".06em",
            textTransform: "uppercase",
            color: "var(--fg-2)",
            fontWeight: 600,
          }}
        >
          Спросить у агента
        </span>
        <span style={{ flex: 1 }} />
        <span style={{ fontSize: 11, color: "var(--fg-3)" }}>
          контекст стадии{" "}
          <span className="mono" style={{ color: "var(--fg-1)" }}>
            {stageLabel}
          </span>{" "}
          прикладывается автоматически
        </span>
      </div>
      <div
        style={{
          border: "1px solid var(--border-strong)",
          borderRadius: "var(--r-md)",
          background: "var(--bg-0)",
          padding: 10,
        }}
      >
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={`Уточнить у ${agentName} — что именно сделано и почему`}
          rows={3}
          style={{
            width: "100%",
            background: "transparent",
            border: 0,
            outline: 0,
            resize: "none",
            color: "var(--fg-0)",
            font: "inherit",
            fontSize: 13,
            lineHeight: 1.5,
          }}
        />
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginTop: 6,
            paddingTop: 8,
            borderTop: "1px solid var(--border-soft)",
          }}
        >
          <span className="hint">⌘+Enter — отправить</span>
          <span style={{ flex: 1 }} />
          <button
            type="button"
            className="topbar-btn primary"
            disabled
            title="скоро будет"
            style={{ opacity: 0.5, cursor: "not-allowed" }}
          >
            Задать вопрос
          </button>
        </div>
      </div>
    </div>
  );
}
