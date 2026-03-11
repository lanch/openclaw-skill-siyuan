"""Tool-level wrappers for SiYuan actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .client import SiyuanClient


@dataclass(frozen=True)
class ToolContext:
    client: SiyuanClient


def list_notebooks(ctx: ToolContext) -> dict[str, Any]:
    return {"notebooks": ctx.client.list_notebooks()}


def create_document(
    ctx: ToolContext,
    notebook_id: str,
    doc_path: str,
    title: str,
    markdown: str,
) -> dict[str, Any]:
    return ctx.client.create_document(
        notebook_id=notebook_id,
        doc_path=doc_path,
        title=title,
        markdown=markdown,
    )


def search_documents(ctx: ToolContext, query: str, limit: int = 10) -> dict[str, Any]:
    return {"blocks": ctx.client.search_blocks(query=query, limit=limit)}


ToolFunc = Callable[..., dict[str, Any]]

TOOL_REGISTRY: dict[str, ToolFunc] = {
    "list_notebooks": list_notebooks,
    "create_document": create_document,
    "search_documents": search_documents,
}


def run_tool(ctx: ToolContext, tool_name: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
    if tool_name not in TOOL_REGISTRY:
        raise KeyError(f"Unknown tool: {tool_name}")

    payload = args or {}
    return TOOL_REGISTRY[tool_name](ctx, **payload)
