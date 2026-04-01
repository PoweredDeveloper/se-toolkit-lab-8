---
name: observability
description: Investigate errors and latency using VictoriaLogs and VictoriaTraces via MCP tools
always: true
---

# Observability skill

Use **`mcp_obs_*`** tools to answer questions about production health, recent errors, and slow or failed requests. Do not guess — query telemetry first when the user asks about errors, outages, or “what went wrong”.

## “What went wrong?” / “Check system health”

When the user asks **What went wrong?**, **Check system health**, or similar **without** a narrower scope, run a **single coherent investigation** (not a tool dump):

1. **`mcp_obs_logs_error_count`** — Use a **short, fresh** window (`time_window`: `5m` or `10m`). Include **`service_name`: `"Learning Management Service"`** when the failure is likely LMS/API-related (e.g. after listing labs/items failed in chat).
2. **`mcp_obs_logs_search`** — If errors exist, query a tight LogsQL window on that service, e.g. `_time:10m service.name:"Learning Management Service" severity:ERROR | limit 20`, and read **`event`**, **`_msg`**, **`path`**, **`status`**, and **`otelTraceID`**.
3. **`mcp_obs_traces_get`** — Take the **most relevant** `otelTraceID` from those log lines and load the trace. Name the **failing span** / operation (e.g. SQLAlchemy `SELECT`, DB client) and whether the trace shows a database or connectivity failure.
4. **Summarize** in one short answer that explicitly cites **both** log evidence (what the log line says) **and** trace evidence (which service, which operation failed). **Do not paste raw JSON.**

**Trust telemetry over misleading API messages.** The HTTP layer may return a generic **404 “Items not found”** (or similar) while VictoriaLogs and VictoriaTraces still show a **real PostgreSQL / SQLAlchemy / connection** failure. Prefer what logs and traces say when they disagree with a vague client error.

## Proactive health checks (same chat, `cron` tool)

When the user asks for a **recurring health check** in the **current WebChat session** (e.g. every 2 minutes), use the built-in **`cron`** tool — not `HEARTBEAT.md` and not `nanobot cron` via exec. Follow **`AGENTS.md`**: use the current session’s **user id** and **channel** (WebChat).

Each run should: call **`mcp_obs_logs_error_count`** with a window matching the interval (e.g. **`time_window`: `2m`** for a 2-minute cadence), optionally **`mcp_obs_logs_search`** / **`mcp_obs_traces_get`** if errors appear, then post a **short** summary in chat. If there are no recent errors, say the system looks healthy.

## Tools (VictoriaLogs / VictoriaTraces)

| Tool | Purpose |
|------|---------|
| `mcp_obs_logs_error_count` | Quick check: how many **ERROR** logs per `service.name` in a time window (e.g. `10m`, `1h`). Prefer **`service_name: "Learning Management Service"`** when the user means the LMS backend. |
| `mcp_obs_logs_search` | Full **LogsQL** search — use for details, `event`, `trace_id`, and messages after you know errors exist. |
| `mcp_obs_traces_list` | Recent traces for a Jaeger **service** name (same string as `service.name` in logs, e.g. `"Learning Management Service"`). |
| `mcp_obs_traces_get` | Load one trace by **trace ID** from a log row. |

## Strategy

1. **Scoped errors** — For “any LMS backend errors in the last 10 minutes?”, call **`logs_error_count`** with `time_window: "10m"` and `service_name: "Learning Management Service"` (adjust the service string if logs use a different name).
2. **If count is zero** — Say so clearly. Optionally run **`logs_search`** with a narrow query to confirm, e.g. `_time:10m service.name:"Learning Management Service"`.
3. **If errors exist** — Use **`logs_search`** with a tight time filter and `severity:ERROR` (or search `event` / `_msg`) to pull a few representative lines. Copy **`trace_id`** when present.
4. **Trace drill-down** — Call **`traces_get`** with the OpenTelemetry trace id from the log row. In VictoriaLogs exports this is usually **`otelTraceID`** (sometimes shown as `trace_id` in docs); pass the **hex string** unchanged into **`traces_get`**.
5. **Response style** — Summarize in plain language: service, time range, count, one or two example events, and what the trace shows. **Do not paste huge JSON**; extract only relevant fields (`event`, `status`, `path`, `error`, span names, duration).

## LogsQL hints

- Time filter: `_time:10m`, `_time:1h`.
- Backend name in this stack is usually **`Learning Management Service`** (`BACKEND_NAME` / OpenTelemetry `service.name`).
- Useful fields: `service.name`, `severity`, `event`, `otelTraceID`, `_msg`.
- If `severity:ERROR` returns nothing but the user sees failures, try **`logs_search`** without severity or filter on `event` / status codes from `request_completed`.

## UI vs tools

The VictoriaLogs and VictoriaTraces web UIs are for humans; students use them in Parts A–B. In chat, always prefer these MCP tools instead of inventing log lines.
