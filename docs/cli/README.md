# CLI Usage

Use the Python package CLI when the host can run Python, uv, and project dependencies. This is the preferred contract for AI agents that need TestRail access from a shell.

## Install

```bash
git clone https://github.com/antuking/testrail-mcp.git
cd testrail-mcp
uv sync
```

Create `.env` in the repository root or export credentials in the shell:

```env
TESTRAIL_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your-email@example.com
TESTRAIL_API_KEY=your-api-key
```

Validate credentials without calling TestRail:

```bash
uv run testrail-mcp-cli check-config --compact
```

## Agent Contract

Give AI agents this instruction instead of pasting the full MCP catalog:

```text
Use testrail-mcp-cli for all TestRail access. Do not use curl, requests, axios, or raw HTTP. Credentials are already available through TESTRAIL_URL, TESTRAIL_USERNAME, and TESTRAIL_API_KEY. Start with catalog --compact, describe one method only when needed, and keep outputs small with --fields, --limit, --compact, --summary, or --output-file.
```

## Discover Entities

Prefer compact discovery to reduce input and output tokens:

```bash
uv run testrail-mcp-cli catalog --compact
uv run testrail-mcp-cli catalog --entity cases --compact
uv run testrail-mcp-cli describe get_cases --compact
uv run testrail-mcp-cli recipes
uv run testrail-mcp-cli guide
```

Use the verbose catalog only when full signatures and docs are needed:

```bash
uv run testrail-mcp-cli entities
uv run testrail-mcp-cli entities --format json
```

## Call TestRail Methods

Each `call` maps to a method on the packaged TestRail client. Parameters use `key=value`; JSON values are parsed automatically.

```bash
uv run testrail-mcp-cli call get_projects --compact

uv run testrail-mcp-cli call get_cases \
  project_id=1 \
  suite_id=2 \
  --limit 50 \
  --fields id,title,section_id \
  --compact

uv run testrail-mcp-cli call add_run \
  project_id=1 \
  data='{"suite_id":2,"name":"Agent run","include_all":true}' \
  --compact
```

## Pass Credentials Per Call

```bash
uv run testrail-mcp-cli call get_project \
  --url https://your-instance.testrail.io \
  --username your-email@example.com \
  --api-key your-api-key \
  project_id=1 \
  --fields id,name \
  --compact
```

## Token-Saving Output Controls

Use `--fields` to keep only important fields:

```bash
uv run testrail-mcp-cli call get_runs \
  project_id=1 \
  --fields id,name,is_completed,created_on \
  --compact
```

Use `--summary` when the agent only needs the response shape:

```bash
uv run testrail-mcp-cli call get_runs project_id=1 --summary --compact
```

Use `--output-file` for large responses so stdout only contains file metadata:

```bash
uv run testrail-mcp-cli call get_cases \
  project_id=1 \
  suite_id=2 \
  --output-file /tmp/cases.json \
  --compact
```

## Run The MCP Server Locally

```bash
uv run testrail-mcp
```

## MCP Client Integration With Local uv

Use these examples when every AI client can run `uv` and this repository locally.

Replace these values first:

```text
<REPO_PATH>        Absolute path to this repository
<TESTRAIL_URL>    https://your-instance.testrail.io
<TESTRAIL_USER>   your-email@example.com
<TESTRAIL_KEY>    your-api-key
```

### Codex CLI

```bash
codex mcp add testrail \
  --env TESTRAIL_URL=<TESTRAIL_URL> \
  --env TESTRAIL_USERNAME=<TESTRAIL_USER> \
  --env TESTRAIL_API_KEY=<TESTRAIL_KEY> \
  -- uv --directory <REPO_PATH> run testrail-mcp
```

Equivalent `~/.codex/config.toml`:

```toml
[mcp_servers.testrail]
command = "uv"
args = ["--directory", "<REPO_PATH>", "run", "testrail-mcp"]

[mcp_servers.testrail.env]
TESTRAIL_URL = "<TESTRAIL_URL>"
TESTRAIL_USERNAME = "<TESTRAIL_USER>"
TESTRAIL_API_KEY = "<TESTRAIL_KEY>"
```

Verify:

```bash
codex mcp list
```

### Claude Code

```bash
claude mcp add --transport stdio --scope local \
  --env TESTRAIL_URL=<TESTRAIL_URL> \
  --env TESTRAIL_USERNAME=<TESTRAIL_USER> \
  --env TESTRAIL_API_KEY=<TESTRAIL_KEY> \
  testrail -- uv --directory <REPO_PATH> run testrail-mcp
```

Project-scoped `.mcp.json`:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "uv",
      "args": ["--directory", "<REPO_PATH>", "run", "testrail-mcp"],
      "env": {
        "TESTRAIL_URL": "<TESTRAIL_URL>",
        "TESTRAIL_USERNAME": "<TESTRAIL_USER>",
        "TESTRAIL_API_KEY": "<TESTRAIL_KEY>"
      }
    }
  }
}
```

Verify:

```bash
claude mcp list
claude mcp get testrail
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
    "testrail": {
      "command": "uv",
      "args": ["--directory", "<REPO_PATH>", "run", "testrail-mcp"],
      "env": {
        "TESTRAIL_URL": "<TESTRAIL_URL>",
        "TESTRAIL_USERNAME": "<TESTRAIL_USER>",
        "TESTRAIL_API_KEY": "<TESTRAIL_KEY>"
      }
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
    "testrail": {
      "command": "uv",
      "args": ["--directory", "<REPO_PATH>", "run", "testrail-mcp"],
      "env": {
        "TESTRAIL_URL": "<TESTRAIL_URL>",
        "TESTRAIL_USERNAME": "<TESTRAIL_USER>",
        "TESTRAIL_API_KEY": "<TESTRAIL_KEY>"
      }
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
    "testrail": {
      "command": "uv",
      "args": ["--directory", "<REPO_PATH>", "run", "testrail-mcp"],
      "env": {
        "TESTRAIL_URL": "<TESTRAIL_URL>",
        "TESTRAIL_USERNAME": "<TESTRAIL_USER>",
        "TESTRAIL_API_KEY": "<TESTRAIL_KEY>"
      }
    }
  }
}
```

Refresh Windsurf MCP servers and check that TestRail tools appear in Cascade.

## References

- [Codex MCP support](https://github.com/openai/codex/blob/main/codex-rs/README.md#model-context-protocol-support)
- [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)
- [Antigravity MCP docs](https://antigravity.google/docs/mcp)
- [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol)
- [Windsurf Cascade MCP docs](https://docs.windsurf.com/windsurf/cascade/mcp)
