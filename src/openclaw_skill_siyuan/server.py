"""Minimal server entrypoint for local tool dispatch."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .client import SiyuanAPIError, SiyuanClient
from .config import SiyuanConfig
from .tools import ToolContext, run_tool


def handle_request(request: dict[str, Any], ctx: ToolContext) -> dict[str, Any]:
    tool_name = request.get("tool")
    if not isinstance(tool_name, str) or not tool_name:
        return {"ok": False, "error": "Field 'tool' must be a non-empty string"}

    args = request.get("args", {})
    if not isinstance(args, dict):
        return {"ok": False, "error": "Field 'args' must be an object"}

    try:
        result = run_tool(ctx, tool_name, args)
    except (KeyError, TypeError, SiyuanAPIError) as exc:
        return {"ok": False, "error": str(exc)}

    return {"ok": True, "result": result}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dispatch SiYuan tools by JSON request")
    parser.add_argument(
        "--request",
        type=str,
        help="JSON request, e.g. '{\"tool\": \"list_notebooks\", \"args\": {}}'",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    raw_request = args.request if args.request is not None else sys.stdin.read().strip()
    if not raw_request:
        print(json.dumps({"ok": False, "error": "Missing JSON request"}))
        return 1

    try:
        request = json.loads(raw_request)
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "error": f"Invalid JSON: {exc}"}))
        return 1

    if not isinstance(request, dict):
        print(json.dumps({"ok": False, "error": "Request must be a JSON object"}))
        return 1

    config = SiyuanConfig.from_env()
    with SiyuanClient(config) as client:
        ctx = ToolContext(client=client)
        response = handle_request(request, ctx)

    print(json.dumps(response, ensure_ascii=False))
    return 0 if response.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
