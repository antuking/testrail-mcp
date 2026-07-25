"""Shell CLI helpers for TestRail MCP sub-agent workflows."""
from __future__ import annotations

import argparse
import base64
import inspect
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from dotenv import load_dotenv

from testrail_mcp.client import TestRailClient

CREDENTIAL_ENV_VARS = ("TESTRAIL_URL", "TESTRAIL_USERNAME", "TESTRAIL_API_KEY")

RECIPES: Dict[str, List[str]] = {
    "projects": [
        "testrail-mcp-cli call get_projects --compact",
        "testrail-mcp-cli call get_project project_id=1 --fields id,name,announcement --compact",
    ],
    "cases": [
        "testrail-mcp-cli call get_cases project_id=1 suite_id=2 limit=50 --fields id,title,section_id,priority_id --compact",
        "testrail-mcp-cli call get_case case_id=123 --fields id,title,section_id,custom_steps,custom_expected",
    ],
    "runs": [
        "testrail-mcp-cli call get_runs project_id=1 --fields id,name,is_completed,created_on --compact",
        "testrail-mcp-cli call get_run run_id=123 --fields id,name,passed_count,failed_count,untested_count",
    ],
    "results": [
        "testrail-mcp-cli call get_results_for_run run_id=123 limit=50 --fields id,test_id,status_id,created_on,comment --compact",
        "testrail-mcp-cli call add_result_for_case run_id=123 case_id=456 data='{\"status_id\":1,\"comment\":\"Passed by sub-agent\"}'",
    ],
    "docker": [
        "docker pull ghcr.io/antuking/testrail-mcp:latest",
        "docker run --rm --env-file .env ghcr.io/antuking/testrail-mcp:latest testrail-cli catalog --compact",
        "TESTRAIL_MCP_DOCKER_IMAGE=ghcr.io/antuking/testrail-mcp:latest ./scripts/testrail-cli catalog --compact",
        "testrail-mcp-cli docker-build --tag testrail-mcp:local",
        "docker run --rm --env-file .env testrail-mcp:local testrail-cli catalog --compact",
        "docker run --rm --env-file .env testrail-mcp:local testrail-cli call get_projects --compact",
        "./scripts/testrail-cli catalog --compact",
    ],
}


def _json_default(value: Any) -> Any:
    """Serialize common non-JSON response values for shell consumers."""
    if isinstance(value, bytes):
        return {
            "type": "bytes",
            "encoding": "base64",
            "content": base64.b64encode(value).decode("ascii"),
        }
    if isinstance(value, Path):
        return str(value)
    return str(value)


def _parse_jsonish(value: str) -> Any:
    """Parse JSON values while keeping plain strings ergonomic for key=value args."""
    text = value.strip()
    if not text:
        return ""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return value


def _parse_key_value_pairs(pairs: Iterable[str]) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(
                f"Invalid parameter {pair!r}. Use key=value, e.g. project_id=1."
            )
        key, value = pair.split("=", 1)
        if not key:
            raise SystemExit(f"Invalid empty key in parameter {pair!r}.")
        kwargs[key.replace("-", "_")] = _parse_jsonish(value)
    return kwargs


def _load_credentials(args: argparse.Namespace) -> Tuple[str, str, str]:
    load_dotenv()
    url = args.url or os.getenv("TESTRAIL_URL")
    username = args.username or os.getenv("TESTRAIL_USERNAME")
    api_key = args.api_key or os.getenv("TESTRAIL_API_KEY")
    missing = [
        name
        for name, value in (
            ("TESTRAIL_URL/--url", url),
            ("TESTRAIL_USERNAME/--username", username),
            ("TESTRAIL_API_KEY/--api-key", api_key),
        )
        if not value
    ]
    if missing:
        raise SystemExit(
            "Missing TestRail credentials: "
            + ", ".join(missing)
            + ". Provide env vars, a .env file, or explicit CLI flags."
        )
    return str(url), str(username), str(api_key)


def _callable_signature(member: Any) -> str:
    signature = inspect.signature(member)
    params = list(signature.parameters.values())
    if params and params[0].name == "self":
        params = params[1:]
    return str(signature.replace(parameters=params))


def _iter_client_methods() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    seen = set()
    for cls in TestRailClient.__mro__:
        module = getattr(cls, "__module__", "")
        if not module.startswith("testrail_mcp.client"):
            continue
        entity = module.rsplit(".", 1)[-1]
        if entity in {"base", "__init__", "client"}:
            continue
        for name, member in inspect.getmembers(cls, inspect.isfunction):
            if name.startswith("_") or name in seen:
                continue
            seen.add(name)
            signature = inspect.signature(member)
            params = [
                param
                for param in signature.parameters.values()
                if param.name != "self"
            ]
            rows.append(
                {
                    "entity": entity,
                    "method": name,
                    "signature": _callable_signature(member),
                    "doc": inspect.getdoc(member) or "",
                    "params": params,
                }
            )
    rows.sort(key=lambda row: (row["entity"], row["method"]))
    return rows


def _method_lookup() -> Dict[str, Dict[str, Any]]:
    return {row["method"]: row for row in _iter_client_methods()}


def _entity_catalog(verbose: bool = True) -> Dict[str, List[Any]]:
    catalog: Dict[str, List[Any]] = {}
    for row in _iter_client_methods():
        if verbose:
            value: Any = {
                "method": row["method"],
                "signature": row["signature"],
                "doc": row["doc"],
            }
        else:
            value = row["method"]
        catalog.setdefault(row["entity"], []).append(value)
    return catalog




def _annotation_label(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty:
        return ""
    if hasattr(annotation, "__name__"):
        return annotation.__name__
    return str(annotation).replace("typing.", "").replace("<class '", "").replace("'>", "")


def _default_value(value: Any) -> Any:
    if value is inspect.Parameter.empty:
        return None
    if value is None or isinstance(value, (str, int, float, bool, list, dict)):
        return value
    return str(value)


def _required_param_names(row: Dict[str, Any]) -> List[str]:
    required: List[str] = []
    for param in row["params"]:
        if param.default is inspect.Parameter.empty:
            required.append(param.name)
    return required


def _example_for_method(row: Dict[str, Any]) -> str:
    args = " ".join(f"{name}=<{name}>" for name in _required_param_names(row))
    suffix = f" {args}" if args else ""
    return f"testrail-mcp-cli call {row['method']}{suffix} --compact"


def _print_json(data: Any, compact: bool = False) -> None:
    if compact:
        print(json.dumps(data, separators=(",", ":"), sort_keys=True, default=_json_default))
    else:
        print(json.dumps(data, indent=2, sort_keys=True, default=_json_default))


def _first_list_key(data: Dict[str, Any]) -> Optional[str]:
    preferred = (
        "projects",
        "cases",
        "sections",
        "runs",
        "tests",
        "results",
        "plans",
        "suites",
        "milestones",
        "users",
        "groups",
        "datasets",
        "labels",
        "attachments",
    )
    for key in preferred:
        if isinstance(data.get(key), list):
            return key
    for key, value in data.items():
        if isinstance(value, list):
            return key
    return None


def _select_from_item(item: Any, fields: Sequence[str]) -> Any:
    if not isinstance(item, dict):
        return item
    return {field: item.get(field) for field in fields if field in item}


def _select_fields(data: Any, fields: Sequence[str]) -> Any:
    if not fields:
        return data
    if isinstance(data, list):
        return [_select_from_item(item, fields) for item in data]
    if isinstance(data, dict):
        list_key = _first_list_key(data)
        if list_key:
            shaped = dict(data)
            shaped[list_key] = [_select_from_item(item, fields) for item in data[list_key]]
            return shaped
        return _select_from_item(data, fields)
    return data


def _count_items(data: Any) -> Optional[int]:
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        list_key = _first_list_key(data)
        if list_key:
            return len(data[list_key])
    return None


def _limit_items(data: Any, max_items: Optional[int]) -> Any:
    if max_items is None:
        return data
    if isinstance(data, list):
        return data[:max_items]
    if isinstance(data, dict):
        list_key = _first_list_key(data)
        if list_key:
            shaped = dict(data)
            original = len(data[list_key])
            shaped[list_key] = data[list_key][:max_items]
            if original > max_items:
                shaped["_cli_truncated"] = True
                shaped["_cli_original_items"] = original
                shaped["_cli_returned_items"] = max_items
            return shaped
    return data


def _write_output_file(path: str, data: Any, compact: bool) -> Dict[str, Any]:
    output_path = Path(path)
    if isinstance(data, bytes):
        output_path.write_bytes(data)
        return {"ok": True, "output_file": str(output_path), "bytes": len(data)}
    text = json.dumps(
        data,
        indent=None if compact else 2,
        separators=(",", ":") if compact else None,
        sort_keys=True,
        default=_json_default,
    )
    output_path.write_text(text + "\n", encoding="utf-8")
    meta: Dict[str, Any] = {
        "ok": True,
        "output_file": str(output_path),
        "bytes": len(text.encode("utf-8")),
    }
    item_count = _count_items(data)
    if item_count is not None:
        meta["items"] = item_count
    return meta


def _summarize_result(data: Any) -> Dict[str, Any]:
    if isinstance(data, bytes):
        return {"type": "bytes", "bytes": len(data)}
    if isinstance(data, list):
        preview = data[:3]
        return {"type": "list", "items": len(data), "preview": preview}
    if isinstance(data, dict):
        list_key = _first_list_key(data)
        summary: Dict[str, Any] = {"type": "object", "keys": sorted(data.keys())}
        if list_key:
            summary["list_key"] = list_key
            summary["items"] = len(data[list_key])
            summary["preview"] = data[list_key][:3]
        return summary
    return {"type": type(data).__name__, "value": data}


def cmd_catalog(args: argparse.Namespace) -> int:
    catalog = _entity_catalog(verbose=False)
    if args.entity:
        catalog = {args.entity: catalog.get(args.entity, [])}
    _print_json(catalog, compact=args.compact)
    return 0


def cmd_describe(args: argparse.Namespace) -> int:
    methods = _method_lookup()
    row = methods.get(args.method)
    if not row:
        available = ", ".join(sorted(methods))
        raise SystemExit(f"Unknown client method {args.method!r}. Available: {available}")
    params = []
    for param in row["params"]:
        params.append(
            {
                "name": param.name,
                "required": param.default is inspect.Parameter.empty,
                "default": _default_value(param.default),
                "annotation": _annotation_label(param.annotation),
            }
        )
    _print_json(
        {
            "entity": row["entity"],
            "method": row["method"],
            "signature": row["signature"],
            "doc": row["doc"],
            "parameters": params,
            "example": _example_for_method(row),
            "token_saving_tip": "Use --fields, --limit, --compact, or --output-file on call outputs.",
        },
        compact=args.compact,
    )
    return 0


def cmd_entities(args: argparse.Namespace) -> int:
    catalog = _entity_catalog(verbose=True)
    if args.format == "json":
        _print_json(
            {
                "credentials": list(CREDENTIAL_ENV_VARS),
                "call_pattern": "testrail-mcp-cli call <method> key=value ...",
                "compact_discovery": "testrail-mcp-cli catalog --compact",
                "method_details": "testrail-mcp-cli describe <method>",
                "docker_call_pattern": "docker run --rm --env-file .env testrail-mcp:local testrail-cli call <method> key=value ...",
                "entities": catalog,
            },
            compact=args.compact,
        )
        return 0

    print("TestRail MCP CLI entity catalog")
    print("Credentials: .env or TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY")
    print("Compact discovery: testrail-mcp-cli catalog --compact")
    print("Method details: testrail-mcp-cli describe <method>")
    print("Call pattern: testrail-mcp-cli call <method> key=value ...")
    for entity, methods in catalog.items():
        print(f"\n[{entity}]")
        for method in methods:
            print(f"  - {method['method']}{method['signature']}")
    return 0


def cmd_guide(args: argparse.Namespace) -> int:
    guide = """TestRail MCP CLI guide for parallel AI sub-agents

Stable contract:
  - Use testrail-mcp-cli for all TestRail access.
  - Do not call TestRail through curl, requests, axios, or raw HTTP.
  - Credentials come from .env or TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY.
  - Start with compact discovery: testrail-mcp-cli catalog --compact.
  - Ask for one method only when needed: testrail-mcp-cli describe <method> --compact.
  - Keep outputs small with --fields, --limit, --compact, --summary, or --output-file.

Common commands:
  testrail-mcp-cli catalog --compact
  testrail-mcp-cli describe get_cases --compact
  testrail-mcp-cli call get_cases project_id=1 suite_id=2 limit=50 --fields id,title --compact
  testrail-mcp-cli call get_runs project_id=1 --fields id,name,is_completed --compact
  testrail-mcp-cli call get_cases project_id=1 suite_id=2 --output-file /tmp/cases.json --compact

Docker for multiple sub-agents:
  docker pull ghcr.io/antuking/testrail-mcp:latest
  docker run --rm --env-file .env ghcr.io/antuking/testrail-mcp:latest testrail-cli catalog --compact
  TESTRAIL_MCP_DOCKER_IMAGE=ghcr.io/antuking/testrail-mcp:latest ./scripts/testrail-cli catalog --compact
  testrail-mcp-cli docker-build --tag testrail-mcp:local
  docker run --rm --env-file .env testrail-mcp:local testrail-cli catalog --compact
  ./scripts/testrail-cli catalog --compact

Parallel guidance:
  - Prefer read/list/get calls in parallel.
  - Coordinate write calls so two agents do not update/delete the same TestRail object.
  - Pass explicit project_id, suite_id, run_id, case_id, etc. in each call.
  - Capture compact JSON stdout or output files as handoff artifacts.
"""
    print(guide.strip())
    return 0


def cmd_recipes(args: argparse.Namespace) -> int:
    if args.topic:
        recipes = {args.topic: RECIPES.get(args.topic, [])}
    else:
        recipes = RECIPES
    if args.format == "json":
        _print_json(recipes, compact=args.compact)
        return 0
    for topic, commands in recipes.items():
        print(f"[{topic}]")
        for command in commands:
            print(f"  {command}")
        print()
    return 0


def cmd_check_config(args: argparse.Namespace) -> int:
    url, username, api_key = _load_credentials(args)
    _print_json(
        {
            "ok": True,
            "url": url,
            "username": username,
            "api_key_present": bool(api_key),
            "api_key_preview": f"...{api_key[-4:]}" if len(api_key) >= 4 else "***",
        },
        compact=args.compact,
    )
    return 0


def cmd_call(args: argparse.Namespace) -> int:
    url, username, api_key = _load_credentials(args)
    client = TestRailClient(url, username, api_key)
    method = getattr(client, args.method, None)
    methods = _method_lookup()
    if method is None or args.method.startswith("_") or not callable(method):
        available = ", ".join(sorted(methods))
        raise SystemExit(f"Unknown client method {args.method!r}. Available: {available}")

    positional: List[Any] = []
    keyword: Dict[str, Any] = {}
    if args.args_json:
        parsed = json.loads(args.args_json)
        if isinstance(parsed, list):
            positional.extend(parsed)
        elif isinstance(parsed, dict):
            keyword.update(parsed)
        else:
            raise SystemExit("--args-json must be a JSON array or object")
    if args.kwargs_json:
        parsed_kwargs = json.loads(args.kwargs_json)
        if not isinstance(parsed_kwargs, dict):
            raise SystemExit("--kwargs-json must be a JSON object")
        keyword.update(parsed_kwargs)
    keyword.update(_parse_key_value_pairs(args.params))

    row = methods[args.method]
    method_param_names = {param.name for param in row["params"]}
    if args.limit is not None and "limit" in method_param_names and "limit" not in keyword:
        keyword["limit"] = args.limit

    result = method(*positional, **keyword)
    shaped = _select_fields(result, _parse_fields(args.fields))
    shaped = _limit_items(shaped, args.limit)
    if args.summary:
        shaped = _summarize_result(shaped)

    if args.output_file:
        _print_json(_write_output_file(args.output_file, shaped, args.compact), compact=True)
    else:
        _print_json(shaped, compact=args.compact)
    return 0


def _parse_fields(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [field.strip() for field in value.split(",") if field.strip()]


def cmd_docker_build(args: argparse.Namespace) -> int:
    context = Path(args.context).resolve() if args.context else Path.cwd().resolve()
    if not (context / "Dockerfile").exists():
        context = Path(__file__).resolve().parent.parent
    if not (context / "Dockerfile").exists():
        raise SystemExit("Could not find a Dockerfile. Pass --context /path/to/repo.")
    docker_bin = _find_docker_binary()
    if not docker_bin:
        raise SystemExit(
            "Docker CLI not found. Install Docker, add it to PATH, or set DOCKER_BIN."
        )
    cmd = [docker_bin, "build", "-t", args.tag, str(context)]
    if args.platform:
        cmd[2:2] = ["--platform", args.platform]
    if args.print_only:
        print(" ".join(cmd))
        return 0
    return subprocess.call(cmd)


def _find_docker_binary() -> Optional[str]:
    explicit = os.getenv("DOCKER_BIN")
    if explicit:
        return explicit
    found = shutil.which("docker")
    if found:
        return found
    for candidate in ("/opt/homebrew/bin/docker", "/usr/local/bin/docker"):
        if Path(candidate).exists():
            return candidate
    return None


def add_credential_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--url", help="TestRail base URL; falls back to TESTRAIL_URL")
    parser.add_argument(
        "--username", help="TestRail username/email; falls back to TESTRAIL_USERNAME"
    )
    parser.add_argument("--api-key", help="TestRail API key; falls back to TESTRAIL_API_KEY")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="testrail-mcp-cli",
        description="Shell wrappers for TestRail MCP sub-agent workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog = subparsers.add_parser("catalog", help="Print compact entity/method catalog")
    catalog.add_argument("--entity", help="Only include one entity, e.g. cases")
    catalog.add_argument("--compact", action="store_true", help="Print compact JSON")
    catalog.set_defaults(func=cmd_catalog)

    describe = subparsers.add_parser("describe", help="Describe one client method")
    describe.add_argument("method", help="Client method name, e.g. get_cases")
    describe.add_argument("--compact", action="store_true", help="Print compact JSON")
    describe.set_defaults(func=cmd_describe)

    entities = subparsers.add_parser("entities", help="List all client entities/methods")
    entities.add_argument("--format", choices=("text", "json"), default="text")
    entities.add_argument("--compact", action="store_true", help="Print compact JSON")
    entities.set_defaults(func=cmd_entities)

    guide = subparsers.add_parser("guide", help="Print AI-agent shell usage guidelines")
    guide.set_defaults(func=cmd_guide)

    recipes = subparsers.add_parser("recipes", help="Print short task-oriented examples")
    recipes.add_argument("topic", nargs="?", help="Optional topic: projects, cases, runs, results, docker")
    recipes.add_argument("--format", choices=("text", "json"), default="text")
    recipes.add_argument("--compact", action="store_true", help="Print compact JSON")
    recipes.set_defaults(func=cmd_recipes)

    check = subparsers.add_parser(
        "check-config", help="Validate credentials without calling TestRail"
    )
    add_credential_args(check)
    check.add_argument("--compact", action="store_true", help="Print compact JSON")
    check.set_defaults(func=cmd_check_config)

    call = subparsers.add_parser(
        "call", help="Call a TestRail client method and print JSON"
    )
    add_credential_args(call)
    call.add_argument("method", help="Client method name, e.g. get_project")
    call.add_argument(
        "params",
        nargs="*",
        help="Method parameters as key=value; values may be JSON",
    )
    call.add_argument(
        "--args-json",
        help="JSON array for positional args, or object for keyword args",
    )
    call.add_argument("--kwargs-json", help="JSON object merged into keyword args")
    call.add_argument("--fields", help="Comma-separated fields to keep in object/list results")
    call.add_argument(
        "--limit",
        type=int,
        help="Limit list output; also passed as method limit when supported and not already set",
    )
    call.add_argument("--compact", action="store_true", help="Print compact JSON")
    call.add_argument("--summary", action="store_true", help="Print a small shape/preview summary")
    call.add_argument(
        "--output-file", help="Write JSON/bytes to a file and print only file metadata"
    )
    call.set_defaults(func=cmd_call)

    docker_build = subparsers.add_parser(
        "docker-build", help="Build a reusable local Docker image for sub-agents"
    )
    docker_build.add_argument("--tag", default="testrail-mcp:local")
    docker_build.add_argument("--context", help="Build context; defaults to current repo")
    docker_build.add_argument("--platform", help="Optional docker build platform")
    docker_build.add_argument(
        "--print-only",
        action="store_true",
        help="Print the docker command without running it",
    )
    docker_build.set_defaults(func=cmd_docker_build)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except SystemExit:
        raise
    except Exception as exc:
        _print_json({"ok": False, "error_type": type(exc).__name__, "error": str(exc)}, compact=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
