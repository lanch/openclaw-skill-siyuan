from __future__ import annotations

import pytest

from openclaw_skill_siyuan.tools import ToolContext, run_tool


class FakeClient:
    def list_notebooks(self):
        return [{"id": "nb-1", "name": "Default"}]

    def create_document(self, notebook_id: str, doc_path: str, title: str, markdown: str):
        return {
            "id": "doc-1",
            "notebook": notebook_id,
            "path": doc_path,
            "title": title,
            "markdown": markdown,
        }

    def search_blocks(self, query: str, limit: int = 10):
        return [{"id": "blk-1", "content": query, "limit": limit}]


def test_run_tool_list_notebooks():
    ctx = ToolContext(client=FakeClient())
    result = run_tool(ctx, "list_notebooks")
    assert result["notebooks"][0]["id"] == "nb-1"


def test_run_tool_create_document():
    ctx = ToolContext(client=FakeClient())
    result = run_tool(
        ctx,
        "create_document",
        {
            "notebook_id": "nb-1",
            "doc_path": "/notes/demo",
            "title": "Demo",
            "markdown": "# Demo",
        },
    )
    assert result["title"] == "Demo"


def test_run_tool_unknown_name():
    ctx = ToolContext(client=FakeClient())
    with pytest.raises(KeyError, match="Unknown tool"):
        run_tool(ctx, "missing_tool")
