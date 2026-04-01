# Multi-stage uv build (see backend/Dockerfile and qwen-code-api/Dockerfile).

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY --from=workspace pyproject.toml uv.lock /app/
COPY --from=workspace mcp/mcp-lms /app/mcp/mcp-lms
COPY --from=workspace mcp/mcp-obs /app/mcp/mcp-obs
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol /app/nanobot-websocket-channel/nanobot-channel-protocol
COPY --from=workspace nanobot-websocket-channel/mcp-webchat /app/nanobot-websocket-channel/mcp-webchat
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat /app/nanobot-websocket-channel/nanobot-webchat

COPY pyproject.toml /app/nanobot/pyproject.toml

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

COPY . /app/nanobot/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# Default workspace files for entrypoint when /host/nanobot-workspace is unavailable.
COPY workspace /opt/nanobot-workspace-default

ARG REGISTRY_PREFIX_DOCKER_HUB
ARG APP_UID=1000
ARG APP_GID=1000
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

ARG APP_UID=1000
ARG APP_GID=1000
RUN groupadd --system --gid ${APP_GID} nonroot \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
WORKDIR /app/nanobot

CMD ["python", "/app/nanobot/entrypoint.py"]
