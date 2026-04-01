"""Resolve VictoriaLogs / VictoriaTraces base URLs from environment."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    victorialogs_base: str
    victoriatraces_base: str


def resolve_settings() -> Settings:
    vlogs = os.environ.get("NANOBOT_VICTORIALOGS_URL", "").strip().rstrip("/")
    vtraces = os.environ.get("NANOBOT_VICTORIATRACES_URL", "").strip().rstrip("/")
    if not vlogs:
        raise RuntimeError(
            "VictoriaLogs URL not configured. Set NANOBOT_VICTORIALOGS_URL."
        )
    if not vtraces:
        raise RuntimeError(
            "VictoriaTraces URL not configured. Set NANOBOT_VICTORIATRACES_URL."
        )
    return Settings(victorialogs_base=vlogs, victoriatraces_base=vtraces)
