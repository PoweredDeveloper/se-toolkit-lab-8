"""HTTP clients for VictoriaLogs (LogsQL) and VictoriaTraces (Jaeger API)."""

from __future__ import annotations

import json
from typing import Any

import httpx


class ObservabilityClient:
    """Thin async wrapper around VictoriaLogs and VictoriaTraces HTTP APIs."""

    def __init__(self, victorialogs_base: str, victoriatraces_base: str) -> None:
        self._vlogs = victorialogs_base.rstrip("/")
        self._vtraces = victoriatraces_base.rstrip("/")
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))

    async def aclose(self) -> None:
        await self._client.aclose()

    async def logs_search(self, query: str, limit: int) -> list[dict[str, Any]]:
        """Run a LogsQL query; response is JSON-lines."""
        url = f"{self._vlogs}/select/logsql/query"
        resp = await self._client.post(
            url,
            data={"query": query, "limit": str(limit)},
        )
        resp.raise_for_status()
        out: list[dict[str, Any]] = []
        for line in resp.text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out

    async def logs_error_count(
        self,
        time_window: str,
        service_name: str | None,
        sample_limit: int,
    ) -> dict[str, Any]:
        """Sample ERROR logs in a time window and aggregate counts by service.name."""
        q = f"_time:{time_window} severity:ERROR"
        if service_name:
            esc = service_name.replace("\\", "\\\\").replace('"', '\\"')
            q += f' service.name:"{esc}"'
        cap = max(1, min(sample_limit, 5000))
        rows = await self.logs_search(q, cap)
        counts: dict[str, int] = {}
        for row in rows:
            key = row.get("service.name")
            if key is None:
                key = row.get("service_name", "(unknown)")
            sk = str(key)
            counts[sk] = counts.get(sk, 0) + 1
        return {
            "time_window": time_window,
            "logs_ql_filter": q,
            "error_rows_sampled": len(rows),
            "errors_by_service": counts,
        }

    async def traces_list(self, service: str, limit: int) -> Any:
        url = f"{self._vtraces}/select/jaeger/api/traces"
        resp = await self._client.get(
            url,
            params={"service": service, "limit": str(limit)},
        )
        resp.raise_for_status()
        return resp.json()

    async def traces_get(self, trace_id: str) -> Any:
        tid = trace_id.strip()
        url = f"{self._vtraces}/select/jaeger/api/traces/{tid}"
        resp = await self._client.get(url)
        resp.raise_for_status()
        return resp.json()
