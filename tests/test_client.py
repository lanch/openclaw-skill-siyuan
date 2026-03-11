from __future__ import annotations

import httpx
import pytest

from openclaw_skill_siyuan.client import SiyuanAPIError, SiyuanClient
from openclaw_skill_siyuan.config import SiyuanConfig


def make_client(handler):
    config = SiyuanConfig(base_url="http://siyuan.test", token="test-token", timeout=2.0)
    http_client = httpx.Client(
        base_url=config.base_url,
        timeout=config.timeout,
        headers=config.auth_headers(),
        transport=httpx.MockTransport(handler),
    )
    return SiyuanClient(config=config, http_client=http_client)


def test_request_success_and_auth_header():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/notebook/lsNotebooks"
        assert request.headers["Authorization"] == "Token test-token"
        return httpx.Response(200, json={"code": 0, "data": {"notebooks": [{"id": "nb-1"}]}})

    client = make_client(handler)
    result = client.request("/api/notebook/lsNotebooks")
    assert result["notebooks"][0]["id"] == "nb-1"


def test_request_raises_for_api_error_code():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"code": 1, "msg": "bad request"})

    client = make_client(handler)
    with pytest.raises(SiyuanAPIError, match="bad request"):
        client.request("/api/notebook/lsNotebooks")


def test_request_raises_for_http_error():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    client = make_client(handler)
    with pytest.raises(SiyuanAPIError, match="Request failed"):
        client.request("/api/notebook/lsNotebooks")
