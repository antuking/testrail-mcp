# Curl Agent Guide

Use this guide only for manual debugging, hosted MCP smoke checks, or direct REST comparison.

Rules for AI agents:

- Do not choose curl as the default TestRail access method.
- Prefer `docs/cli/AGENT.md` when Python and uv are available.
- Prefer `docs/docker/AGENT.md` when Docker is available.
- Use curl only when the user explicitly asks for raw HTTP debugging or when comparing CLI behavior against direct TestRail REST.
- Never paste API keys into conversation output.
- Keep curl responses out of the conversation when they are large; save to a file or summarize.
- Read `docs/curl/README.md` before using curl examples.

Preferred equivalent for agents:

```bash
testrail-cli catalog --compact
testrail-cli call get_projects --compact
testrail-cli call get_cases project_id=1 suite_id=2 --fields id,title --limit 50 --compact
```
