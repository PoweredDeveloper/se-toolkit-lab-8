#!/usr/bin/env python3
"""Resolve Docker env vars into nanobot config, then exec nanobot gateway."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

_HOST_WS = Path("/host/nanobot-workspace")
_SEED_WS = Path("/opt/nanobot-workspace-default")


def _sync_workspace(target: Path) -> None:
    """Populate writable workspace from read-only host mount or image seed."""
    target.mkdir(parents=True, exist_ok=True)
    if _HOST_WS.is_dir() and (_HOST_WS / "AGENTS.md").is_file():
        for child in _HOST_WS.iterdir():
            dest = target / child.name
            if child.is_dir():
                shutil.copytree(child, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(child, dest)
        return
    if _SEED_WS.is_dir() and (_SEED_WS / "AGENTS.md").is_file() and not (target / "AGENTS.md").is_file():
        shutil.copytree(_SEED_WS, target, dirs_exist_ok=True)


def _int_env(name: str, default: str) -> int:
    return int(os.environ.get(name, default).strip() or default)


def resolve_config() -> Path:
    app_dir = Path(__file__).resolve().parent
    config_path = app_dir / "config.json"
    with config_path.open(encoding="utf-8") as f:
        config: dict = json.load(f)

    # LLM / provider (custom OpenAI-compatible API)
    custom = config.setdefault("providers", {}).setdefault("custom", {})
    if key := os.environ.get("LLM_API_KEY", "").strip():
        custom["apiKey"] = key
    if base := os.environ.get("LLM_API_BASE_URL", "").strip():
        custom["apiBase"] = base

    agents = config.setdefault("agents", {}).setdefault("defaults", {})
    if model := os.environ.get("LLM_API_MODEL", "").strip():
        agents["model"] = model

    # Gateway
    gw = config.setdefault("gateway", {})
    if host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "").strip():
        gw["host"] = host
    gw["port"] = _int_env("NANOBOT_GATEWAY_CONTAINER_PORT", str(gw.get("port", 18790)))

    # WebChat channel + UI relay (same container as gateway)
    relay_host = os.environ.get("NANOBOT_UI_RELAY_HOST", "127.0.0.1").strip() or "127.0.0.1"
    relay_port = _int_env("NANOBOT_UI_RELAY_PORT", "8766")
    relay_url = os.environ.get("NANOBOT_UI_RELAY_URL", "").strip()
    if not relay_url:
        relay_url = f"http://{relay_host}:{relay_port}/ui-message"
    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "").strip()
    relay_token = os.environ.get("NANOBOT_UI_RELAY_TOKEN", "").strip() or access_key

    channels = config.setdefault("channels", {})
    webchat = channels.setdefault("webchat", {})
    webchat["enabled"] = True
    webchat.setdefault("allowFrom", ["*"])
    webchat["host"] = os.environ.get(
        "NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0"
    ).strip() or "0.0.0.0"
    webchat["port"] = _int_env(
        "NANOBOT_WEBCHAT_CONTAINER_PORT", str(webchat.get("port", 8765))
    )
    webchat["relayHost"] = relay_host
    webchat["relayPort"] = relay_port

    # MCP servers
    tools = config.setdefault("tools", {})
    mcp_servers: dict = {}

    lms_backend = os.environ.get("NANOBOT_LMS_BACKEND_URL", "").strip()
    lms_key = os.environ.get("NANOBOT_LMS_API_KEY", "").strip()
    lms_entry: dict = {"command": "python", "args": ["-m", "mcp_lms"], "env": {}}
    if lms_backend:
        lms_entry["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend
    if lms_key:
        lms_entry["env"]["NANOBOT_LMS_API_KEY"] = lms_key
    mcp_servers["lms"] = lms_entry

    mcp_servers["webchat"] = {
        "command": "python",
        "args": ["-m", "mcp_webchat"],
        "env": {
            "NANOBOT_UI_RELAY_URL": relay_url,
            "NANOBOT_UI_RELAY_TOKEN": relay_token,
        },
    }

    vlogs = os.environ.get("NANOBOT_VICTORIALOGS_URL", "").strip()
    vtraces = os.environ.get("NANOBOT_VICTORIATRACES_URL", "").strip()
    if vlogs and vtraces:
        mcp_servers["obs"] = {
            "command": "python",
            "args": ["-m", "mcp_obs"],
            "env": {
                "NANOBOT_VICTORIALOGS_URL": vlogs,
                "NANOBOT_VICTORIATRACES_URL": vtraces,
            },
        }

    tools["mcpServers"] = mcp_servers

    # Writable path: bind-mounted ./nanobot may be host-owned and not writable by
    # container user (HOST_UID), so default to /tmp instead of app_dir.
    resolved_raw = os.environ.get("NANOBOT_RESOLVED_CONFIG_PATH", "").strip()
    resolved_path = Path(resolved_raw) if resolved_raw else Path("/tmp/config.resolved.json")
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    with resolved_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    return resolved_path


def main() -> None:
    app_dir = Path(__file__).resolve().parent
    workspace = app_dir / "workspace"
    _sync_workspace(workspace)
    resolved = resolve_config()
    print(f"Using config: {resolved}", flush=True)
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved),
            "--workspace",
            str(workspace),
        ],
    )


if __name__ == "__main__":
    main()
