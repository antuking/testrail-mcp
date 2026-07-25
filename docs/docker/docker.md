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

## Parallel Sub-Agent Guidance

- Use Docker for a consistent runtime across many agents.
- Prefer read/list/get calls in parallel.
- Coordinate write calls so two agents do not update or delete the same TestRail object.
- Pass explicit IDs in every call; do not rely on conversational state.
- Use `--fields`, `--limit`, `--compact`, `--summary`, or `--output-file` to keep token usage small.
