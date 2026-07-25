# CLI Agent Guide

Use this guide when the host can run Python, uv, and repository dependencies.

Rules for AI agents:

- Use `uv run testrail-mcp-cli ...` or `uv run testrail-cli ...` for all TestRail access.
- Do not use `curl`, `requests`, `axios`, browser fetch, or raw HTTP for TestRail work.
- Read `docs/cli/cli.md` before calling TestRail methods.
- Start with compact discovery: `uv run testrail-mcp-cli catalog --compact`.
- Describe only one method when needed: `uv run testrail-mcp-cli describe <method> --compact`.
- Keep outputs small with `--fields`, `--limit`, `--compact`, `--summary`, or `--output-file`.
- Pass explicit IDs in every command; do not rely on conversational state.
- Use `.env` or `TESTRAIL_URL`, `TESTRAIL_USERNAME`, and `TESTRAIL_API_KEY` for credentials.

Default workflow:

```bash
uv run testrail-mcp-cli catalog --compact
uv run testrail-mcp-cli describe get_cases --compact
uv run testrail-mcp-cli call get_cases project_id=1 suite_id=2 --fields id,title --limit 50 --compact
```
