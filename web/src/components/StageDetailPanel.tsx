// StageDetailPanel — shows the header, input/output, and the filtered event
// stream for the currently selected stage of an expanded task.

import type { JSX } from "react";
import { Activity, Check, Clock, X } from "lucide-react";

import type { UiEvent, UiStage, UiTask } from "../api";
import { STAGES } from "../stages";
import { formatCost, formatDurationMs, formatTokens } from "../utils";
import AgentBadge from "./AgentBadge";
import AskAgentComposer from "./AskAgentComposer";
import EventStream from "./EventStream";
import StageIO from "./StageIO";

interface Props {
  task: UiTask;
  stageId: string;
  events: UiEvent[];
}

const AGENT_STAGES = new Set(["agent_plan", "agent_implement"]);

function StageSubblock({
  title,
  icon,
  trailing,
  children,
  noPad,
}: {
  title: string;
  icon?: JSX.Element;
  trailing?: JSX.Element;
  children: JSX.Element | null;
  noPad?: boolean;
}): JSX.Element {
  return (
    <div
      style={{
        borderRight: "1px solid var(--border)",
        display: "flex",
        flexDirection: "column",
        minWidth: 0,
      }}
    >
      <div
        style={{
          padding: "8px 14px",
          borderBottom: "1px solid var(--border-soft)",
          display: "flex",
          alignItems: "center",
          gap: 6,
          fontSize: 10,
          letterSpacing: ".08em",
          textTransform: "uppercase",
          fontWeight: 600,
          color: "var(--fg-2)",
          flexShrink: 0,
        }}
      >
        {icon}
        <span>{title}</span>
        <span style={{ flex: 1 }} />
        {trailing}
      </div>
      <div
        style={{
          padding: noPad ? 0 : "10px 14px",
          flex: 1,
          overflow: "hidden",
          minHeight: 0,
        }}
      >
        {children}
      </div>
    </div>
  );
}

export default function StageDetailPanel({ task, stageId, events }: Props): JSX.Element {
  const stage: UiStage = task.stages[stageId] ?? {
    name: stageId,
    status: "pending",
  };
  const stageMeta = STAGES.find((s) => s.id === stageId);
  const isAgentStage = AGENT_STAGES.has(stageId);
  const isPending = stage.status === "pending";
  const isRunning = stage.status === "running";
  const isFailed = stage.status === "failed";
  const isDone = stage.status === "done";

  if (isPending) {
    return (
      <div
        className="card"
        style={{
          padding: "22px 24px",
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        <div
          style={{
            width: 28,
            height: 28,
            borderRadius: "50%",
            background: "var(--bg-2)",
            display: "grid",
            placeItems: "center",
            color: "var(--fg-3)",
          }}
        >
          <Clock className="ico-sm" />
        </div>
        <div>
          <div style={{ fontSize: 13, fontWeight: 500, color: "var(--fg-1)" }}>
            Стадия{" "}
            <span className="mono" style={{ color: "var(--fg-0)" }}>
              {stageMeta?.label ?? stageId}
            </span>{" "}
            — ещё не выполнялась
          </div>
          <div style={{ fontSize: 11.5, color: "var(--fg-2)", marginTop: 2 }}>
            Начнётся после завершения предыдущих стадий.
          </div>
        </div>
      </div>
    );
  }

  const tokensTotal = (stage.tokens_in ?? 0) + (stage.tokens_out ?? 0);

  return (
    <div className="card" style={{ padding: 0, overflow: "hidden" }}>
      {/* Header */}
      <div
        style={{
          padding: "12px 18px",
          borderBottom: "1px solid var(--border)",
          display: "flex",
          alignItems: "center",
          gap: 12,
          background: isRunning
            ? "var(--running-soft)"
            : isFailed
              ? "var(--danger-soft)"
              : "var(--bg-1)",
        }}
      >
        <span
          style={{
            fontSize: 10,
            letterSpacing: ".1em",
            textTransform: "uppercase",
            fontWeight: 700,
            color: isRunning
              ? "var(--running)"
              : isFailed
                ? "var(--danger)"
                : "var(--success)",
          }}
        >
          {stageMeta?.title ?? stageId}
        </span>
        <span className="mono" style={{ color: "var(--fg-3)", fontSize: 11 }}>
          ·
        </span>
        {isRunning && (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              fontSize: 11.5,
              color: "var(--running)",
            }}
          >
            <span className="spinner" />
            идёт сейчас
          </span>
        )}
        {isDone && (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 5,
              fontSize: 11.5,
              color: "var(--success)",
            }}
          >
            <Check className="ico-sm" />
            завершено
          </span>
        )}
        {isFailed && (
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 5,
              fontSize: 11.5,
              color: "var(--danger)",
            }}
          >
            <X className="ico-sm" />
            провал
          </span>
        )}
        <span style={{ flex: 1 }} />

        {stage.agent && <AgentBadge agent={stage.agent} />}

        <div
          className="tabular"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            fontSize: 11,
            color: "var(--fg-2)",
          }}
        >
          {stage.duration_ms != null && (
            <span style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
              <Clock className="ico-sm" />
              {formatDurationMs(stage.duration_ms)}
            </span>
          )}
          {stage.cost_usd != null && stage.cost_usd > 0 && (
            <span>{formatCost(stage.cost_usd)}</span>
          )}
          {tokensTotal > 0 && (
            <span style={{ color: "var(--fg-3)" }}>{formatTokens(tokensTotal)} ток.</span>
          )}
        </div>
      </div>

      {/* Body grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: isAgentStage ? "1fr 1.4fr 1fr" : "1fr 1fr",
          minHeight: 240,
        }}
      >
        <StageSubblock title="Вход">
          <StageIO kind="input" data={stage.input ?? null} />
        </StageSubblock>

        {isAgentStage && (
          <StageSubblock
            title="Поток событий"
            icon={<Activity className="ico-sm" style={{ color: "var(--accent)" }} />}
            trailing={
              isRunning ? (
                <span
                  style={{
                    color: "var(--running)",
                    fontSize: 10.5,
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 4,
                  }}
                >
                  <span className="dot dot-running" style={{ width: 5, height: 5 }} />
                  live
                </span>
              ) : (
                <span className="mono dim" style={{ fontSize: 10.5 }}>
                  {events.length}
                </span>
              )
            }
            noPad
          >
            <EventStream events={events} style="telegram" />
          </StageSubblock>
        )}

        <StageSubblock title="Выход">
          <StageIO kind="output" data={stage.output ?? null} />
        </StageSubblock>
      </div>

      {/* Traceback */}
      {isFailed && stage.error && (
        <div style={{ padding: "0 14px 14px" }}>
          <pre className="trace">{stage.error}</pre>
        </div>
      )}

      {/* Composer stub (UI-only) */}
      {isAgentStage && <AskAgentComposer agent={stage.agent} stageLabel={stageMeta?.label ?? stageId} />}
    </div>
  );
}
