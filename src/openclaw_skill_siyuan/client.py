"""Low-level SiYuan HTTP client based on the official API document."""

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

    @staticmethod
    def _normalize_endpoint(endpoint: str) -> str:
        cleaned = endpoint.strip()
        if not cleaned:
            raise SiyuanAPIError("API endpoint cannot be empty")
        return cleaned if cleaned.startswith("/") else f"/{cleaned}"

    def request(self, endpoint: str, payload: dict[str, Any] | None = None) -> Any:
        api = self._normalize_endpoint(endpoint)
        data = payload or {}
        try:
            response = self._client.post(api, json=data)
            response.raise_for_status()
            body = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SiyuanAPIError(f"Request failed for {api}: {exc}") from exc

        if not isinstance(body, dict):
            raise SiyuanAPIError(f"Invalid response for {api}: expected JSON object")

        code = body.get("code", 0)
        if code != 0:
            msg = body.get("msg", "Unknown SiYuan error")
            raise SiyuanAPIError(f"SiYuan API error {code} on {api}: {msg}")

        return body.get("data")

    # Generic fallback for unsupported/new endpoints.
    def call_api(self, endpoint: str, payload: dict[str, Any] | None = None) -> Any:
        return self.request(endpoint, payload)

    # notebook
    def list_notebooks(self) -> list[dict[str, Any]]:
        data = self.request("/api/notebook/lsNotebooks")
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/notebook/lsNotebooks")
        notebooks = data.get("notebooks", [])
        if not isinstance(notebooks, list):
            raise SiyuanAPIError("Invalid notebooks list from /api/notebook/lsNotebooks")
        return notebooks

    def open_notebook(self, notebook_id: str) -> None:
        self.request("/api/notebook/openNotebook", {"notebook": notebook_id})

    def close_notebook(self, notebook_id: str) -> None:
        self.request("/api/notebook/closeNotebook", {"notebook": notebook_id})

    def rename_notebook(self, notebook_id: str, name: str) -> None:
        self.request("/api/notebook/renameNotebook", {"notebook": notebook_id, "name": name})

    def create_notebook(self, name: str) -> dict[str, Any]:
        data = self.request("/api/notebook/createNotebook", {"name": name})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/notebook/createNotebook")
        return data

    def remove_notebook(self, notebook_id: str) -> None:
        self.request("/api/notebook/removeNotebook", {"notebook": notebook_id})

    def get_notebook_conf(self, notebook_id: str) -> dict[str, Any]:
        data = self.request("/api/notebook/getNotebookConf", {"notebook": notebook_id})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/notebook/getNotebookConf")
        return data

    def set_notebook_conf(self, notebook_id: str, conf: dict[str, Any]) -> dict[str, Any]:
        data = self.request("/api/notebook/setNotebookConf", {"notebook": notebook_id, "conf": conf})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/notebook/setNotebookConf")
        return data

    # filetree
    def create_doc_with_md(self, notebook_id: str, path: str, markdown: str) -> str:
        data = self.request(
            "/api/filetree/createDocWithMd",
            {"notebook": notebook_id, "path": path, "markdown": markdown},
        )
        if not isinstance(data, str):
            raise SiyuanAPIError("Invalid data for /api/filetree/createDocWithMd")
        return data

    def rename_doc(self, notebook_id: str, path: str, title: str) -> None:
        self.request(
            "/api/filetree/renameDoc",
            {"notebook": notebook_id, "path": path, "title": title},
        )

    def rename_doc_by_id(self, doc_id: str, title: str) -> None:
        self.request("/api/filetree/renameDocByID", {"id": doc_id, "title": title})

    def remove_doc(self, notebook_id: str, path: str) -> None:
        self.request("/api/filetree/removeDoc", {"notebook": notebook_id, "path": path})

    def remove_doc_by_id(self, doc_id: str) -> None:
        self.request("/api/filetree/removeDocByID", {"id": doc_id})

    def move_docs(self, from_paths: list[str], to_notebook: str, to_path: str) -> None:
        self.request(
            "/api/filetree/moveDocs",
            {"fromPaths": from_paths, "toNotebook": to_notebook, "toPath": to_path},
        )

    def move_docs_by_id(self, from_ids: list[str], to_id: str) -> None:
        self.request("/api/filetree/moveDocsByID", {"fromIDs": from_ids, "toID": to_id})

    def get_hpath_by_path(self, notebook_id: str, path: str) -> str:
        data = self.request("/api/filetree/getHPathByPath", {"notebook": notebook_id, "path": path})
        if not isinstance(data, str):
            raise SiyuanAPIError("Invalid data for /api/filetree/getHPathByPath")
        return data

    def get_hpath_by_id(self, block_id: str) -> str:
        data = self.request("/api/filetree/getHPathByID", {"id": block_id})
        if not isinstance(data, str):
            raise SiyuanAPIError("Invalid data for /api/filetree/getHPathByID")
        return data

    def get_path_by_id(self, block_id: str) -> dict[str, Any]:
        data = self.request("/api/filetree/getPathByID", {"id": block_id})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/filetree/getPathByID")
        return data

    def get_ids_by_hpath(self, path: str, notebook_id: str) -> list[str]:
        data = self.request("/api/filetree/getIDsByHPath", {"path": path, "notebook": notebook_id})
        if not isinstance(data, list):
            raise SiyuanAPIError("Invalid data for /api/filetree/getIDsByHPath")
        return [str(item) for item in data]

    # block
    def insert_block(
        self,
        data: str,
        data_type: str = "markdown",
        next_id: str = "",
        previous_id: str = "",
        parent_id: str = "",
    ) -> list[dict[str, Any]]:
        result = self.request(
            "/api/block/insertBlock",
            {
                "dataType": data_type,
                "data": data,
                "nextID": next_id,
                "previousID": previous_id,
                "parentID": parent_id,
            },
        )
        if not isinstance(result, list):
            raise SiyuanAPIError("Invalid data for /api/block/insertBlock")
        return result

    def prepend_block(self, parent_id: str, data: str, data_type: str = "markdown") -> list[dict[str, Any]]:
        result = self.request(
            "/api/block/prependBlock",
            {"data": data, "dataType": data_type, "parentID": parent_id},
        )
        if not isinstance(result, list):
            raise SiyuanAPIError("Invalid data for /api/block/prependBlock")
        return result

    def append_block(self, parent_id: str, data: str, data_type: str = "markdown") -> list[dict[str, Any]]:
        result = self.request(
            "/api/block/appendBlock",
            {"data": data, "dataType": data_type, "parentID": parent_id},
        )
        if not isinstance(result, list):
            raise SiyuanAPIError("Invalid data for /api/block/appendBlock")
        return result

    def update_block(self, block_id: str, data: str, data_type: str = "markdown") -> list[dict[str, Any]]:
        result = self.request(
            "/api/block/updateBlock",
            {"dataType": data_type, "data": data, "id": block_id},
        )
        if not isinstance(result, list):
            raise SiyuanAPIError("Invalid data for /api/block/updateBlock")
        return result

    def delete_block(self, block_id: str) -> list[dict[str, Any]]:
        result = self.request("/api/block/deleteBlock", {"id": block_id})
        if not isinstance(result, list):
            raise SiyuanAPIError("Invalid data for /api/block/deleteBlock")
        return result

    def move_block(self, block_id: str, previous_id: str = "", parent_id: str = "") -> list[dict[str, Any]]:
        result = self.request(
            "/api/block/moveBlock",
            {"id": block_id, "previousID": previous_id, "parentID": parent_id},
        )
        if not isinstance(result, list):
            raise SiyuanAPIError("Invalid data for /api/block/moveBlock")
        return result

    def fold_block(self, block_id: str) -> None:
        self.request("/api/block/foldBlock", {"id": block_id})

    def unfold_block(self, block_id: str) -> None:
        self.request("/api/block/unfoldBlock", {"id": block_id})

    def get_block_kramdown(self, block_id: str) -> dict[str, Any]:
        data = self.request("/api/block/getBlockKramdown", {"id": block_id})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/block/getBlockKramdown")
        return data

    def get_child_blocks(self, block_id: str) -> list[dict[str, Any]]:
        data = self.request("/api/block/getChildBlocks", {"id": block_id})
        if not isinstance(data, list):
            raise SiyuanAPIError("Invalid data for /api/block/getChildBlocks")
        return data

    def transfer_block_ref(self, from_id: str, to_id: str, ref_ids: list[str] | None = None) -> None:
        payload: dict[str, Any] = {"fromID": from_id, "toID": to_id}
        if ref_ids is not None:
            payload["refIDs"] = ref_ids
        self.request("/api/block/transferBlockRef", payload)

    # attr
    def set_block_attrs(self, block_id: str, attrs: dict[str, Any]) -> None:
        self.request("/api/attr/setBlockAttrs", {"id": block_id, "attrs": attrs})

    def get_block_attrs(self, block_id: str) -> dict[str, Any]:
        data = self.request("/api/attr/getBlockAttrs", {"id": block_id})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/attr/getBlockAttrs")
        return data

    # query/sqlite
    def query_sql(self, stmt: str) -> list[dict[str, Any]]:
        data = self.request("/api/query/sql", {"stmt": stmt})
        if not isinstance(data, list):
            raise SiyuanAPIError("Invalid data for /api/query/sql")
        return data

    def flush_transaction(self) -> None:
        self.request("/api/sqlite/flushTransaction")

    # template
    def render_template(self, doc_id: str, path: str) -> dict[str, Any]:
        data = self.request("/api/template/render", {"id": doc_id, "path": path})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/template/render")
        return data

    def render_sprig(self, template: str) -> str:
        data = self.request("/api/template/renderSprig", {"template": template})
        if not isinstance(data, str):
            raise SiyuanAPIError("Invalid data for /api/template/renderSprig")
        return data

    # file/export
    def read_dir(self, path: str) -> list[dict[str, Any]]:
        data = self.request("/api/file/readDir", {"path": path})
        if not isinstance(data, list):
            raise SiyuanAPIError("Invalid data for /api/file/readDir")
        return data

    def remove_file(self, path: str) -> None:
        self.request("/api/file/removeFile", {"path": path})

    def rename_file(self, path: str, new_path: str) -> None:
        self.request("/api/file/renameFile", {"path": path, "newPath": new_path})

    def export_md_content(self, doc_id: str) -> dict[str, Any]:
        data = self.request("/api/export/exportMdContent", {"id": doc_id})
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/export/exportMdContent")
        return data

    def export_resources(self, paths: list[str], name: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"paths": paths}
        if name:
            payload["name"] = name
        data = self.request("/api/export/exportResources", payload)
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/export/exportResources")
        return data

    # notification/system
    def push_msg(self, msg: str, timeout: int | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"msg": msg}
        if timeout is not None:
            payload["timeout"] = timeout
        data = self.request("/api/notification/pushMsg", payload)
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/notification/pushMsg")
        return data

    def push_err_msg(self, msg: str, timeout: int | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"msg": msg}
        if timeout is not None:
            payload["timeout"] = timeout
        data = self.request("/api/notification/pushErrMsg", payload)
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/notification/pushErrMsg")
        return data

    def boot_progress(self) -> dict[str, Any]:
        data = self.request("/api/system/bootProgress")
        if not isinstance(data, dict):
            raise SiyuanAPIError("Invalid data for /api/system/bootProgress")
        return data

    def version(self) -> str:
        data = self.request("/api/system/version")
        if not isinstance(data, str):
            raise SiyuanAPIError("Invalid data for /api/system/version")
        return data

    def current_time(self) -> int:
        data = self.request("/api/system/currentTime")
        if not isinstance(data, int):
            raise SiyuanAPIError("Invalid data for /api/system/currentTime")
        return data
