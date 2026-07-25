# Curl Usage

Use curl for manual debugging, hosted HTTP MCP checks, or direct TestRail REST comparisons. AI sub-agents should prefer the CLI or Docker wrapper because those commands provide a stable contract and token-saving output controls.

## Hosted MCP Endpoint

The hosted MCP endpoint is:

```text
https://kyzu-testrail.fastmcp.app/mcp
```

Register it with MCP clients instead of hand-writing JSON-RPC whenever possible:

```bash
codex mcp add --url https://kyzu-testrail.fastmcp.app/mcp kyzu-testrail
claude mcp add --scope local --transport http kyzu-testrail https://kyzu-testrail.fastmcp.app/mcp
gemini mcp add kyzu-testrail https://kyzu-testrail.fastmcp.app/mcp --transport http
```

A minimal protocol smoke request with curl looks like this:

```bash
curl -sS https://kyzu-testrail.fastmcp.app/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"0.1.0"}}}'
```

## Direct TestRail REST Debugging

Use direct REST only for human debugging or comparing CLI behavior. Do not give this as the default instruction to AI sub-agents.

Set credentials:

```bash
export TESTRAIL_URL=https://your-instance.testrail.io
export TESTRAIL_USERNAME=your-email@example.com
export TESTRAIL_API_KEY=your-api-key
```

List projects:

```bash
curl -sS \
  -u "$TESTRAIL_USERNAME:$TESTRAIL_API_KEY" \
  "$TESTRAIL_URL/index.php?/api/v2/get_projects"
```

Get cases:

```bash
curl -sS \
  -u "$TESTRAIL_USERNAME:$TESTRAIL_API_KEY" \
  "$TESTRAIL_URL/index.php?/api/v2/get_cases/1&suite_id=2&limit=50"
```

Add a run:

```bash
curl -sS \
  -u "$TESTRAIL_USERNAME:$TESTRAIL_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{"suite_id":2,"name":"Agent run","include_all":true}' \
  "$TESTRAIL_URL/index.php?/api/v2/add_run/1"
```

## Equivalent CLI Commands

Prefer these equivalents for agents:

```bash
testrail-cli catalog --compact
testrail-cli call get_projects --compact
testrail-cli call get_cases project_id=1 suite_id=2 --limit 50 --fields id,title,section_id --compact
testrail-cli call add_run project_id=1 data='{"suite_id":2,"name":"Agent run","include_all":true}' --compact
```

The CLI equivalents avoid leaking large raw payloads into the conversation and keep credentials in `.env` or environment variables.
