"""Low-level SiYuan HTTP client."""

from __future__ import annotations

from typing import Any

import httpx

from .config import SiyuanConfig


class SiyuanAPIError(RuntimeError):
    """Raised when SiYuan returns an error or an invalid response."""


class SiyuanClient:
    """Thin client around SiYuan HTTP API."""

    def __init__(self, config: SiyuanConfig, http_client: httpx.Client | None = None) -> None:
        self.config = config
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers=config.auth_headers(),
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "SiyuanClient":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def request(self, endpoint: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = payload or {}
        try:
            response = self._client.post(endpoint, json=data)
            response.raise_for_status()
            body = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SiyuanAPIError(f"Request failed for {endpoint}: {exc}") from exc

        if not isinstance(body, dict):
            raise SiyuanAPIError(f"Invalid response for {endpoint}: expected JSON object")

        code = body.get("code", 0)
        if code != 0:
            msg = body.get("msg", "Unknown SiYuan error")
            raise SiyuanAPIError(f"SiYuan API error {code}: {msg}")

        result = body.get("data", {})
        return result if isinstance(result, dict) else {"result": result}

    def list_notebooks(self) -> list[dict[str, Any]]:
        data = self.request("/api/notebook/lsNotebooks")
        notebooks = data.get("notebooks", [])
        return notebooks if isinstance(notebooks, list) else []

    def create_document(
        self,
        notebook_id: str,
        doc_path: str,
        title: str,
        markdown: str,
    ) -> dict[str, Any]:
        return self.request(
            "/api/filetree/createDocWithMd",
            {
                "notebook": notebook_id,
                "path": doc_path,
                "title": title,
                "markdown": markdown,
            },
        )

    def search_blocks(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        data = self.request(
            "/api/search/fullTextSearchBlock",
            {
                "query": query,
                "method": 0,
                "paths": [],
                "types": {"document": True, "heading": True, "paragraph": True},
                "page": 1,
                "pageSize": limit,
            },
        )
        blocks = data.get("blocks", [])
        return blocks if isinstance(blocks, list) else []
