# Docker Agent Guide

Use this guide when the host has Docker, especially when Python, uv, or dependencies are unavailable locally.

Rules for AI agents:

- Use `testrail-cli ...` inside Docker for all TestRail access.
- Prefer the host shim `./scripts/testrail-cli ...` when working from this repository.
- Do not install Python, uv, or package dependencies on the host just to query TestRail.
- Do not use `curl`, `requests`, `axios`, browser fetch, or raw HTTP for TestRail work.
- Read `docs/docker/README.md` before running Docker commands.
- Use a pulled image when available: `ghcr.io/antuking/testrail-mcp:latest`.
- Use `.env` or forwarded `TESTRAIL_URL`, `TESTRAIL_USERNAME`, and `TESTRAIL_API_KEY` for credentials.
- Keep outputs small with `--fields`, `--limit`, `--compact`, `--summary`, or `--output-file`.

Default workflow with a prebuilt image:

```bash
export TESTRAIL_MCP_DOCKER_IMAGE=ghcr.io/antuking/testrail-mcp:latest
./scripts/testrail-cli catalog --compact
./scripts/testrail-cli describe get_cases --compact
./scripts/testrail-cli call get_cases project_id=1 suite_id=2 --fields id,title --limit 50 --compact
```

Default workflow with a local image:

```bash
docker build -t testrail-mcp:local .
./scripts/testrail-cli catalog --compact
```
