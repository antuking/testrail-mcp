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

Example Codex CLI registration:

```bash
codex mcp add testrail_mcp \
  --env TESTRAIL_URL=<TESTRAIL_URL> \
  --env TESTRAIL_USERNAME=<TESTRAIL_USERNAME> \
  --env TESTRAIL_API_KEY=<TESTRAIL_API_KEY> \
  -- uv --directory <REPO_PATH> run testrail-mcp
```
