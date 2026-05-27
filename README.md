# TestRail MCP Server

A Model Context Protocol (MCP) server for TestRail that allows interaction with TestRail's core entities through a standardized protocol.

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

## 🚀 Quick Start (Hosted)

The fastest way to use TestRail MCP is through our hosted instance at `https://horizon.prefect.io/`.

Add it to your favorite AI tools using these commands:

### Codex CLI
```bash
codex mcp add --url https://kyzu-testrail.fastmcp.app/mcp kyzu-testrail
```

### Claude CLI
```bash
claude mcp add --scope local --transport http kyzu-testrail https://kyzu-testrail.fastmcp.app/mcp
```

### Gemini CLI
```bash
gemini mcp add kyzu-testrail https://kyzu-testrail.fastmcp.app/mcp --transport http
```

---

## 🛠️ Local Setup (Self-Hosted)

If you prefer to run the server locally for development or private use.

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) installed on your system.
- TestRail API credentials (URL, Username, API Key).

### 2. Installation
```bash
git clone https://github.com/yourusername/testrail-mcp.git
cd testrail-mcp
uv sync
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
TESTRAIL_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your-email@example.com
TESTRAIL_API_KEY=your-api-key
```

Verify your configuration:
```bash
uv run testrail-mcp --config
```

### 4. Running the Server
```bash
uv run testrail-mcp
```

### 5. Using with MCP Clients (Local)

#### Codex CLI
```bash
codex mcp add testrail_mcp \
  --env TESTRAIL_URL=<TESTRAIL_URL> \
  --env TESTRAIL_USERNAME=<TESTRAIL_USERNAME> \
  --env TESTRAIL_API_KEY=<TESTRAIL_API_KEY> \
  -- uv --directory <REPO_PATH> run testrail-mcp
```

#### Claude Desktop
```json
{
  "mcpServers": {
    "testrail": {
      "command": "uv",
      "args": ["--directory", "<REPO_PATH>", "run", "testrail-mcp"],
      "env": {
        "TESTRAIL_URL": "https://your-instance.testrail.io",
        "TESTRAIL_USERNAME": "your-email@example.com",
        "TESTRAIL_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Cursor / Windsurf
```json
{
  "name": "TestRail MCP",
  "command": "uv",
  "args": ["--directory", "<REPO_PATH>", "run", "testrail-mcp"],
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

## Development

This server is built using:
- [FastMCP](https://github.com/jlowin/fastmcp) - A Python framework for building MCP servers
- [Requests](https://requests.readthedocs.io/) - For HTTP communication
- [python-dotenv](https://github.com/theskumar/python-dotenv) - For environment management
