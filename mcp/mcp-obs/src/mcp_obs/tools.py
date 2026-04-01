"""Tool specs for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.observability import ObservabilityClient


class LogsSearchQuery(BaseModel):
    """LogsQL query for VictoriaLogs."""

    query: str = Field(
        description=(
            "Full LogsQL query. Include a time filter such as _time:10m. "
            "Useful fields include service.name, severity, event, trace_id, _msg."
        )
    )
    limit: int = Field(default=50, ge=1, le=500, description="Max log rows to return.")


class LogsErrorCountQuery(BaseModel):
    time_window: str = Field(
        default="10m",
        description="LogsQL duration suffix for _time, e.g. 10m, 1h.",
    )
    service_name: str | None = Field(
        default=None,
        description=(
            'Optional exact service.name match, e.g. "Learning Management Service". '
            "If omitted, counts all ERROR logs in the window."
        ),
    )
    sample_limit: int = Field(
        default=2000,
        ge=1,
        le=5000,
        description="Max ERROR rows to pull for aggregation (caps cost).",
    )


class TracesListQuery(BaseModel):
    service: str = Field(
        description=(
            "Jaeger service name to list traces for, e.g. the OpenTelemetry "
            'service.name for the LMS backend (often "Learning Management Service").'
        )
    )
    limit: int = Field(default=20, ge=1, le=100)


class TracesGetQuery(BaseModel):
    trace_id: str = Field(
        description="Trace ID from logs (trace_id field) or traces_list results."
    )


ToolPayload = dict[str, Any] | list[Any] | BaseModel
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]

TModel = TypeVar("TModel", bound=BaseModel)


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    q = _require(args, LogsSearchQuery)
    return await client.logs_search(q.query, q.limit)


async def _logs_error_count(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    q = _require(args, LogsErrorCountQuery)
    return await client.logs_error_count(
        q.time_window, q.service_name, q.sample_limit
    )


async def _traces_list(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    q = _require(args, TracesListQuery)
    return await client.traces_list(q.service, q.limit)


async def _traces_get(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    q = _require(args, TracesGetQuery)
    return await client.traces_get(q.trace_id)


def _require(args: BaseModel, typ: type[TModel]) -> TModel:
    if not isinstance(args, typ):
        raise TypeError(f"Expected {typ.__name__}, got {type(args).__name__}")
    return args


TOOL_SPECS: tuple[ToolSpec, ...] = (
    ToolSpec(
        "logs_search",
        "Search VictoriaLogs with a LogsQL query. Returns recent structured log rows as JSON.",
        LogsSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count ERROR-severity logs in a time window, grouped by service.name (sampled).",
        LogsErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces for a Jaeger/OpenTelemetry service from VictoriaTraces.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Fetch one trace by ID (Jaeger JSON) for span hierarchy and errors.",
        TracesGetQuery,
        _traces_get,
    ),
)

TOOLS_BY_NAME = {s.name: s for s in TOOL_SPECS}
