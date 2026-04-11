FROM mwader/static-ffmpeg:7.1 AS ffmpeg-layer
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV PATH="/.venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="/.venv" \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONPATH=/app/src

WORKDIR /app
COPY pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY /src /app/src

FROM python:3.12-slim-bookworm AS runner

COPY --from=ffmpeg-layer /ffmpeg /usr/local/bin/ffmpeg
COPY --from=ffmpeg-layer /ffprobe /usr/local/bin/ffprobe

COPY --from=builder /.venv /.venv
COPY --from=builder /app/src /app/src

ENV PATH="/.venv/bin:$PATH" \
    PYTHONPATH=/app/src

WORKDIR /app/src

EXPOSE 80

CMD ["faststream", "run", "main:app", "--reload"]
