from __future__ import annotations

from openclaw_skill_siyuan.server import handle_request
from openclaw_skill_siyuan.tools import ToolContext


class FakeClient:
    def list_notebooks(self):
        return [{"id": "nb-1"}]


def test_handle_request_success():
    ctx = ToolContext(client=FakeClient())
    response = handle_request({"tool": "list_notebooks", "args": {}}, ctx)
    assert response["ok"] is True
    assert response["result"]["notebooks"][0]["id"] == "nb-1"


def test_handle_request_rejects_invalid_tool_field():
    ctx = ToolContext(client=FakeClient())
    response = handle_request({"tool": "", "args": {}}, ctx)
    assert response["ok"] is False
    assert "tool" in response["error"]
