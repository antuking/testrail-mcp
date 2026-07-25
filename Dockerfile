# Reusable runtime for MCP server + CLI sub-agent workflows.
# Includes Python, uv, the locked dependency environment, and global CLI aliases.
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

# Copy dependency metadata first for better Docker layer reuse.
COPY pyproject.toml uv.lock README.md ./
COPY testrail_mcp ./testrail_mcp

# Install the project and dependencies into /app/.venv using the lockfile.
RUN uv sync --frozen --no-dev \
    && ln -sf /app/.venv/bin/testrail-mcp /usr/local/bin/testrail-mcp \
    && ln -sf /app/.venv/bin/testrail-mcp-cli /usr/local/bin/testrail-mcp-cli \
    && ln -sf /app/.venv/bin/testrail-cli /usr/local/bin/testrail-cli

# Default mode remains the MCP server. Override the command with `testrail-cli ...`
# for shell/sub-agent usage.
CMD ["testrail-mcp"]
