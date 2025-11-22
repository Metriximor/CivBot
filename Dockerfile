FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin
WORKDIR /app
COPY . /app
RUN uv sync
CMD ["uv", "run", "CivBot.py"]
