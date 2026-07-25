# TestRail MCP Server

TestRail MCP gives AI coding agents a safe, compact, and repeatable way to work with TestRail. It exposes TestRail entities through MCP, adds a shell-friendly CLI wrapper for sub-agents, and ships a Docker runtime so teams do not need Python, uv, or dependencies installed on every machine.

## What This Repository Unlocks

- **Broad TestRail entity coverage**: Projects, suites, sections, cases, runs, plans, milestones, tests, results, statuses, datasets, labels, templates, priorities, users, groups, shared steps, configurations, configuration groups, and attachments.
- **MCP server for AI clients**: Register the server in Codex CLI, Claude Code, Antigravity CLI, Cursor, Windsurf, and other MCP-compatible tools.
- **CLI wrapper for sub-agents**: Use `testrail-mcp-cli` or the shorter `testrail-cli` from shell-only agent contexts instead of making raw HTTP requests.
- **Docker-first agent runtime**: Build or pull one image with Python, uv, locked dependencies, the MCP server, and global CLI aliases.
- **Token-saving workflows**: Start with `catalog --compact`, inspect one method with `describe`, and keep responses small with `--fields`, `--limit`, `--compact`, `--summary`, and `--output-file`.
- **Parallel-agent guidance**: Separate docs and `AGENT.md` contracts help multiple AI agents query TestRail without duplicating huge tool catalogs or racing on writes.

## Runtime Choices

| Runtime | Best For | Entry Point |
| --- | --- | --- |
| Hosted HTTP | Fastest MCP client setup | `https://kyzu-testrail.fastmcp.app/mcp` |
| Local uv | Repository development and local MCP stdio | `uv run testrail-mcp` |
| CLI | Shell-only AI agents on hosts with Python and uv | `uv run testrail-mcp-cli ...` or `uv run testrail-cli ...` |
| Docker | Sub-agents and machines without local Python or uv | `docker run ... testrail-cli ...` or `./scripts/testrail-cli ...` |

## Quick Start

### Hosted MCP

```bash
codex mcp add --url https://kyzu-testrail.fastmcp.app/mcp kyzu-testrail
claude mcp add --transport http kyzu-testrail https://kyzu-testrail.fastmcp.app/mcp
```

See [curl usage and hosted HTTP integrations](docs/curl/README.md) for Antigravity CLI, Cursor, and Windsurf config examples.

### Local uv

```bash
git clone https://github.com/antuking/testrail-mcp.git
cd testrail-mcp
uv sync
```

Create `.env`:

```env
TESTRAIL_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your-email@example.com
TESTRAIL_API_KEY=your-api-key
```

Validate the local CLI contract:

```bash
uv run testrail-mcp-cli check-config --compact
uv run testrail-mcp-cli catalog --compact
uv run testrail-mcp-cli describe get_cases --compact
```

Run the local MCP server:

```bash
uv run testrail-mcp
```

See [CLI usage and local uv integrations](docs/cli/README.md) for full client setup examples.

### Docker

Build a reusable image:

```bash
docker build -t testrail-mcp:local .
```

Run the CLI inside Docker:

```bash
docker run --rm --env-file .env testrail-mcp:local \
  testrail-cli catalog --compact
```

Or use the host shim:

```bash
./scripts/testrail-cli catalog --compact
./scripts/testrail-cli call get_projects --compact
```

See [Docker usage and Docker stdio integrations](docs/docker/README.md) for pull/build commands and Codex CLI, Claude Code, Antigravity CLI, Cursor, and Windsurf config examples.

## AI Agent Contract

For shell-only agents, pass one usage-specific guide instead of the whole repository context:

```text
docs/cli/AGENT.md
docs/docker/AGENT.md
docs/curl/AGENT.md
```

Default guidance for sub-agents:

```text
Use testrail-cli for all TestRail access. Do not use curl, requests, axios, browser fetch, or raw HTTP unless the task explicitly asks for HTTP debugging. Start with catalog --compact, describe one method only when needed, and keep outputs small with --fields, --limit, --compact, --summary, or --output-file.
```

## Documentation

- [Docs overview](docs/README.md)
- [CLI usage](docs/cli/README.md): local CLI, token-saving calls, and local uv MCP integration.
- [Docker usage](docs/docker/README.md): reusable Docker runtime, host shim, and Docker stdio MCP integration.
- [Curl usage](docs/curl/README.md): hosted HTTP MCP integration, curl smoke checks, and direct REST debugging.

## Development

This server is built with:

- [FastMCP](https://github.com/jlowin/fastmcp)
- [Requests](https://requests.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [uv](https://github.com/astral-sh/uv)

Useful checks:

```bash
uv run python -m py_compile testrail_mcp/cli.py
/bin/sh -n scripts/testrail-cli
docker build -t testrail-mcp:local .
```
