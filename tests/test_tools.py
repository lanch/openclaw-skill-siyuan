from __future__ import annotations

import pytest

from openclaw_skill_siyuan.tools import ToolContext, list_tools, run_tool


class FakeClient:
    def __init__(self):
        self.last_stmt = ""

    def call_api(self, endpoint: str, payload=None):
        return {"endpoint": endpoint, "payload": payload}

    def list_notebooks(self):
        return [{"id": "nb-1", "name": "Default"}]

    def create_doc_with_md(self, notebook_id: str, path: str, markdown: str):
        assert notebook_id == "nb-1"
        assert path == "/demo/path"
        assert markdown == "# Demo"
        return "doc-1"

    def query_sql(self, stmt: str):
        self.last_stmt = stmt
        return [{"id": "blk-1", "content": "hello"}]

    def rename_doc_by_id(self, doc_id: str, title: str):
        assert doc_id == "doc-1"
        assert title == "Demo"


def test_list_tools_contains_main_entries():
    tools = list_tools()
    assert "call_api" in tools
    assert "list_notebooks" in tools
    assert "create_doc_with_md" in tools
    assert "query_sql" in tools


def test_run_tool_list_notebooks():
    ctx = ToolContext(client=FakeClient())
    result = run_tool(ctx, "list_notebooks")
    assert result["notebooks"][0]["id"] == "nb-1"


def test_run_tool_create_doc_with_md():
    ctx = ToolContext(client=FakeClient())
    result = run_tool(
        ctx,
        "create_doc_with_md",
        {"notebook_id": "nb-1", "path": "/demo/path", "markdown": "# Demo"},
    )
    assert result["id"] == "doc-1"


def test_run_tool_search_documents_uses_sql_fallback():
    client = FakeClient()
    ctx = ToolContext(client=client)
    result = run_tool(ctx, "search_documents", {"query": "hello", "limit": 5})
    assert "FROM blocks" in result["stmt"]
    assert "LIMIT 5" in result["stmt"]
    assert result["rows"][0]["id"] == "blk-1"
    assert client.last_stmt == result["stmt"]


def test_run_tool_call_api_passthrough():
    ctx = ToolContext(client=FakeClient())
    result = run_tool(ctx, "call_api", {"endpoint": "/api/system/version", "payload": {}})
    assert result["data"]["endpoint"] == "/api/system/version"


def test_run_tool_legacy_create_document_alias():
    ctx = ToolContext(client=FakeClient())
    result = run_tool(
        ctx,
        "create_document",
        {
            "notebook_id": "nb-1",
            "doc_path": "/demo/path",
            "title": "Demo",
            "markdown": "# Demo",
        },
    )
    assert result["id"] == "doc-1"


def test_run_tool_unknown_name():
    ctx = ToolContext(client=FakeClient())
    with pytest.raises(KeyError, match="Unknown tool"):
        run_tool(ctx, "missing_tool")
