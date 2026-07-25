# Docker Usage

Use Docker when the host cannot install Python, uv, or project dependencies. The Docker image includes Python, uv, this package, locked dependencies, and global CLI aliases.

Inside the container these commands are available:

```bash
testrail-mcp
testrail-mcp-cli
testrail-cli
```

`testrail-cli` is the short alias intended for AI sub-agents.

## Pull A Published Image

After the GitHub package is published, sub-agents can pull and run it directly:

```bash
docker pull ghcr.io/antuking/testrail-mcp:latest

docker run --rm --env-file .env ghcr.io/antuking/testrail-mcp:latest \
  testrail-cli catalog --compact
```

If the package is private, authenticate first:

```bash
docker login ghcr.io
```

## Build A Local Image

```bash
docker build -t testrail-mcp:local .
```

When uv is available on the host, this helper prints or runs the same build command:

```bash
uv run testrail-mcp-cli docker-build --tag testrail-mcp:local --print-only
uv run testrail-mcp-cli docker-build --tag testrail-mcp:local
```

## Run CLI Commands In Docker

```bash
docker run --rm --env-file .env testrail-mcp:local \
  testrail-cli catalog --compact

docker run --rm --env-file .env testrail-mcp:local \
  testrail-cli call get_projects --compact

docker run --rm --env-file .env testrail-mcp:local \
  testrail-cli call get_cases project_id=1 suite_id=2 \
    --limit 50 \
    --fields id,title,section_id \
    --compact
```

## Use The Host Shim

The repo includes `scripts/testrail-cli` for hosts that have Docker but do not have Python, uv, or dependencies.

Use a pulled image:

```bash
export TESTRAIL_MCP_DOCKER_IMAGE=ghcr.io/antuking/testrail-mcp:latest
./scripts/testrail-cli catalog --compact
```

Or use a local image:

```bash
docker build -t testrail-mcp:local .
./scripts/testrail-cli catalog --compact
./scripts/testrail-cli call get_projects --compact
```

Make the host command name exactly `testrail-cli` for the current shell:

```bash
export PATH="$PWD/scripts:$PATH"
testrail-cli catalog --compact
```

The shim passes `.env` when present, forwards `TESTRAIL_URL`, `TESTRAIL_USERNAME`, and `TESTRAIL_API_KEY`, and mounts the current directory at `/workspace` so `--output-file` can write artifacts back to the host.

## Run The MCP Server In Docker

The image default command is the stdio MCP server:

```bash
docker run --rm -i --env-file .env testrail-mcp:local
```

Explicit form:

```bash
docker run --rm -i --env-file .env testrail-mcp:local testrail-mcp
```

## MCP Client Integration With Docker stdio

Use these examples when multiple agents should share the same runtime or when local Python, uv, and dependencies are unavailable.

Replace these values first:

```text
<REPO_PATH>        Absolute path to this repository
<IMAGE>            testrail-mcp:local or ghcr.io/antuking/testrail-mcp:latest
<TESTRAIL_URL>     https://your-instance.testrail.io
<TESTRAIL_USER>    your-email@example.com
<TESTRAIL_KEY>     your-api-key
```

### Codex CLI

With `.env`:

```bash
codex mcp add testrail-docker -- \
  docker run --rm -i --env-file <REPO_PATH>/.env <IMAGE> testrail-mcp
```

With explicit environment:

```bash
codex mcp add testrail-docker \
  --env TESTRAIL_URL=<TESTRAIL_URL> \
  --env TESTRAIL_USERNAME=<TESTRAIL_USER> \
  --env TESTRAIL_API_KEY=<TESTRAIL_KEY> \
  -- docker run --rm -i \
    -e TESTRAIL_URL \
    -e TESTRAIL_USERNAME \
    -e TESTRAIL_API_KEY \
    <IMAGE> testrail-mcp
```

Equivalent `~/.codex/config.toml` with `.env`:

```toml
[mcp_servers.testrail-docker]
command = "docker"
args = ["run", "--rm", "-i", "--env-file", "<REPO_PATH>/.env", "<IMAGE>", "testrail-mcp"]
```

Verify:

```bash
codex mcp list
```

### Claude Code

```bash
claude mcp add --transport stdio --scope local testrail-docker -- \
  docker run --rm -i --env-file <REPO_PATH>/.env <IMAGE> testrail-mcp
```

Project-scoped `.mcp.json`:

```json
{
  "mcpServers": {
    "testrail-docker": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env-file",
        "<REPO_PATH>/.env",
        "<IMAGE>",
        "testrail-mcp"
      ]
    }
  }
}
```

Verify:

```bash
claude mcp list
claude mcp get testrail-docker
```

Inside Claude Code, use `/mcp` to inspect connection status.

### Antigravity CLI

Global config:

```text
~/.gemini/config/mcp_config.json
```

Workspace config:

```text
.agents/mcp_config.json
```

```json
{
  "mcpServers": {
    "testrail-docker": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env-file",
        "<REPO_PATH>/.env",
        "<IMAGE>",
        "testrail-mcp"
      ]
    }
  }
}
```

Verify from Antigravity CLI with `/mcp` and reload the MCP configuration.

### Cursor

Project config:

```text
.cursor/mcp.json
```

Global config:

```text
~/.cursor/mcp.json
```

```json
{
  "mcpServers": {
    "testrail-docker": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env-file",
        "<REPO_PATH>/.env",
        "<IMAGE>",
        "testrail-mcp"
      ]
    }
  }
}
```

Verify in Cursor settings under MCP tools, then ask the agent to list available TestRail tools.

### Windsurf

Config path on macOS/Linux:

```text
~/.codeium/windsurf/mcp_config.json
```

```json
{
  "mcpServers": {
    "testrail-docker": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env-file",
        "<REPO_PATH>/.env",
        "<IMAGE>",
        "testrail-mcp"
      ]
    }
  }
}
```

Refresh Windsurf MCP servers and check that TestRail tools appear in Cascade.

## Parallel Sub-Agent Guidance

- Use Docker for a consistent runtime across many agents.
- Prefer read/list/get calls in parallel.
- Coordinate write calls so two agents do not update or delete the same TestRail object.
- Pass explicit IDs in every call; do not rely on conversational state.
- Use `--fields`, `--limit`, `--compact`, `--summary`, or `--output-file` to keep token usage small.

## References

- [Codex MCP support](https://github.com/openai/codex/blob/main/codex-rs/README.md#model-context-protocol-support)
- [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- [Antigravity MCP docs](https://antigravity.google/docs/mcp)
- [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol)
- [Windsurf Cascade MCP docs](https://docs.windsurf.com/windsurf/cascade/mcp)
