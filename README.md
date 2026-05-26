# TestRail MCP Server

A Model Context Protocol (MCP) server for TestRail that allows interaction with TestRail's core entities through a standardized protocol.

## Quick Start

```bash
uv sync
cat > .env << 'EOF'
TESTRAIL_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your-email@example.com
TESTRAIL_API_KEY=your-api-key
EOF
uv run testrail-mcp
```

## Features

- **Full CRUD Support**: Comprehensive Create, Read, Update, and Delete operations for all core TestRail entities.
- **Access to TestRail entities**:
  - Projects, Suites, Sections, Cases
  - Runs, Plans, Milestones
  - Tests, Results, Statuses
  - Datasets, Labels, Templates, Priorities
  - Users, Groups, Shared Steps
  - Configurations & Configuration Groups
  - Attachments
- **Smart Filtering**: Enhanced `get_tests` with internal `section_id` filtering (cross-referencing tests with section cases).
- **Status Helpers**: Resolve numeric status IDs instantly using `get_status_id_by_name`.
- **v6.2+ Enhanced Support**: Support for `refs` in runs and plans, and material change validation.
- **Full MCP Support**: Standardized protocol for use with any MCP client (Claude Desktop, Cursor, Windsurf, etc.).

## Local Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/testrail-mcp.git
   cd testrail-mcp
   ```

2. Install dependencies with uv:

   ```bash
   uv sync
   ```

## Configuration

The TestRail MCP server requires specific environment variables to authenticate with your TestRail instance. These must be set before running the server.

1. Create a `.env` file in the root directory of the project:

   ```env
   TESTRAIL_URL=https://your-instance.testrail.io
   TESTRAIL_USERNAME=your-email@example.com
   TESTRAIL_API_KEY=your-api-key
   ```

   Notes:
   - `TESTRAIL_URL` should be the full URL to your TestRail instance (for example, `https://example.testrail.io`)
   - `TESTRAIL_USERNAME` is your TestRail email address used for login
   - `TESTRAIL_API_KEY` is your TestRail API key (not your password)

2. Verify configuration locally:

   ```bash
   uv run testrail-mcp --config
   ```

## Usage

### Running the Server Locally

From inside this repository:

```bash
uv run testrail-mcp
```

From any directory:

```bash
uv --directory /absolute/path/to/testrail-mcp run testrail-mcp
```

This starts the MCP server in stdio mode.

### Using with MCP Clients (Local Repo)

Set `REPO_PATH` to your local clone path (for example, `/Users/you/dev/testrail-mcp`).

#### Codex CLI

```bash
codex mcp add testrail_mcp \
  --env TESTRAIL_URL=<TESTRAIL_URL> \
  --env TESTRAIL_USERNAME=<TESTRAIL_USERNAME> \
  --env TESTRAIL_API_KEY=<TESTRAIL_API_KEY> \
  -- uv --directory <REPO_PATH> run testrail-mcp
```

Or in `config.toml`:

```toml
[mcp_servers.testrail_mcp]
command = "uv"
args = ["--directory", "<REPO_PATH>", "run", "testrail-mcp"]

[mcp_servers.testrail_mcp.env]
TESTRAIL_API_KEY = "<TESTRAIL_API_KEY>"
TESTRAIL_URL = "<TESTRAIL_URL>"
TESTRAIL_USERNAME = "<TESTRAIL_USERNAME>"
```

#### Claude Desktop

```json
{
  "mcpServers": {
    "testrail": {
      "command": "uv",
      "args": [
        "--directory",
        "<REPO_PATH>",
        "run",
        "testrail-mcp"
      ],
      "env": {
        "TESTRAIL_URL": "https://your-instance.testrail.io",
        "TESTRAIL_USERNAME": "your-email@example.com",
        "TESTRAIL_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Cursor

```json
{
  "name": "TestRail MCP",
  "command": "uv",
  "args": [
    "--directory",
    "<REPO_PATH>",
    "run",
    "testrail-mcp"
  ],
  "env": {
    "TESTRAIL_URL": "https://your-instance.testrail.io",
    "TESTRAIL_USERNAME": "your-email@example.com",
    "TESTRAIL_API_KEY": "your-api-key"
  }
}
```

#### Windsurf

```json
{
  "name": "TestRail MCP",
  "command": "uv",
  "args": [
    "--directory",
    "<REPO_PATH>",
    "run",
    "testrail-mcp"
  ],
  "env": {
    "TESTRAIL_URL": "https://your-instance.testrail.io",
    "TESTRAIL_USERNAME": "your-email@example.com",
    "TESTRAIL_API_KEY": "your-api-key"
  }
}
```

#### Gemini CLI

```bash
gemini mcp add testrail \
  --env TESTRAIL_URL=<TESTRAIL_URL> \
  --env TESTRAIL_USERNAME=<TESTRAIL_USERNAME> \
  --env TESTRAIL_API_KEY=<TESTRAIL_API_KEY> \
  -- uv --directory <REPO_PATH> run testrail-mcp
```

Or in `config.yaml`:

```yaml
mcpServers:
  testrail:
    command: "uv"
    args:
      - "--directory"
      - "<REPO_PATH>"
      - "run"
      - "testrail-mcp"
    env:
      TESTRAIL_URL: "https://your-instance.testrail.io"
      TESTRAIL_USERNAME: "your-email@example.com"
      TESTRAIL_API_KEY: "your-api-key"
```

#### Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector \
  -e TESTRAIL_URL=<your-url> \
  -e TESTRAIL_USERNAME=<your-username> \
  -e TESTRAIL_API_KEY=<your-api-key> \
  uv --directory <REPO_PATH> run testrail-mcp
```

## Development

This server is built using:

- [FastMCP](https://github.com/jlowin/fastmcp) - A Python framework for building MCP servers
- [Requests](https://requests.readthedocs.io/) - For HTTP communication with TestRail API
- [python-dotenv](https://github.com/theskumar/python-dotenv) - For environment variable management
