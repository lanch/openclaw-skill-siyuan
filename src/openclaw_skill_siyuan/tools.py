"""Tool-level wrappers for SiYuan actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .client import SiyuanClient


@dataclass(frozen=True)
class ToolContext:
    client: SiyuanClient


ToolFunc = Callable[..., dict[str, Any]]


def _ok() -> dict[str, Any]:
    return {"ok": True}


def call_api(ctx: ToolContext, endpoint: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"data": ctx.client.call_api(endpoint, payload)}


# notebook tools

def list_notebooks(ctx: ToolContext) -> dict[str, Any]:
    return {"notebooks": ctx.client.list_notebooks()}


def open_notebook(ctx: ToolContext, notebook_id: str) -> dict[str, Any]:
    ctx.client.open_notebook(notebook_id)
    return _ok()


def close_notebook(ctx: ToolContext, notebook_id: str) -> dict[str, Any]:
    ctx.client.close_notebook(notebook_id)
    return _ok()


def create_notebook(ctx: ToolContext, name: str) -> dict[str, Any]:
    return {"data": ctx.client.create_notebook(name)}


def rename_notebook(ctx: ToolContext, notebook_id: str, name: str) -> dict[str, Any]:
    ctx.client.rename_notebook(notebook_id, name)
    return _ok()


def remove_notebook(ctx: ToolContext, notebook_id: str) -> dict[str, Any]:
    ctx.client.remove_notebook(notebook_id)
    return _ok()


def get_notebook_conf(ctx: ToolContext, notebook_id: str) -> dict[str, Any]:
    return {"data": ctx.client.get_notebook_conf(notebook_id)}


def set_notebook_conf(ctx: ToolContext, notebook_id: str, conf: dict[str, Any]) -> dict[str, Any]:
    return {"data": ctx.client.set_notebook_conf(notebook_id, conf)}


# doc tools

def create_doc_with_md(ctx: ToolContext, notebook_id: str, path: str, markdown: str) -> dict[str, Any]:
    return {"id": ctx.client.create_doc_with_md(notebook_id, path, markdown)}


def rename_doc(ctx: ToolContext, notebook_id: str, path: str, title: str) -> dict[str, Any]:
    ctx.client.rename_doc(notebook_id, path, title)
    return _ok()


def rename_doc_by_id(ctx: ToolContext, doc_id: str, title: str) -> dict[str, Any]:
    ctx.client.rename_doc_by_id(doc_id, title)
    return _ok()


def remove_doc(ctx: ToolContext, notebook_id: str, path: str) -> dict[str, Any]:
    ctx.client.remove_doc(notebook_id, path)
    return _ok()


def remove_doc_by_id(ctx: ToolContext, doc_id: str) -> dict[str, Any]:
    ctx.client.remove_doc_by_id(doc_id)
    return _ok()


def move_docs(ctx: ToolContext, from_paths: list[str], to_notebook: str, to_path: str) -> dict[str, Any]:
    ctx.client.move_docs(from_paths, to_notebook, to_path)
    return _ok()


def move_docs_by_id(ctx: ToolContext, from_ids: list[str], to_id: str) -> dict[str, Any]:
    ctx.client.move_docs_by_id(from_ids, to_id)
    return _ok()


def get_hpath_by_path(ctx: ToolContext, notebook_id: str, path: str) -> dict[str, Any]:
    return {"hpath": ctx.client.get_hpath_by_path(notebook_id, path)}


def get_hpath_by_id(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    return {"hpath": ctx.client.get_hpath_by_id(block_id)}


def get_path_by_id(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    return {"data": ctx.client.get_path_by_id(block_id)}


def get_ids_by_hpath(ctx: ToolContext, notebook_id: str, path: str) -> dict[str, Any]:
    return {"ids": ctx.client.get_ids_by_hpath(path, notebook_id)}


# block tools

def insert_block(
    ctx: ToolContext,
    data: str,
    data_type: str = "markdown",
    next_id: str = "",
    previous_id: str = "",
    parent_id: str = "",
) -> dict[str, Any]:
    return {
        "operations": ctx.client.insert_block(
            data=data,
            data_type=data_type,
            next_id=next_id,
            previous_id=previous_id,
            parent_id=parent_id,
        )
    }


def prepend_block(ctx: ToolContext, parent_id: str, data: str, data_type: str = "markdown") -> dict[str, Any]:
    return {"operations": ctx.client.prepend_block(parent_id=parent_id, data=data, data_type=data_type)}


def append_block(ctx: ToolContext, parent_id: str, data: str, data_type: str = "markdown") -> dict[str, Any]:
    return {"operations": ctx.client.append_block(parent_id=parent_id, data=data, data_type=data_type)}


def update_block(ctx: ToolContext, block_id: str, data: str, data_type: str = "markdown") -> dict[str, Any]:
    return {"operations": ctx.client.update_block(block_id=block_id, data=data, data_type=data_type)}


def delete_block(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    return {"operations": ctx.client.delete_block(block_id)}


def move_block(ctx: ToolContext, block_id: str, previous_id: str = "", parent_id: str = "") -> dict[str, Any]:
    return {"operations": ctx.client.move_block(block_id=block_id, previous_id=previous_id, parent_id=parent_id)}


def fold_block(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    ctx.client.fold_block(block_id)
    return _ok()


def unfold_block(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    ctx.client.unfold_block(block_id)
    return _ok()


def get_block_kramdown(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    return {"data": ctx.client.get_block_kramdown(block_id)}


def get_child_blocks(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    return {"children": ctx.client.get_child_blocks(block_id)}


def transfer_block_ref(
    ctx: ToolContext,
    from_id: str,
    to_id: str,
    ref_ids: list[str] | None = None,
) -> dict[str, Any]:
    ctx.client.transfer_block_ref(from_id=from_id, to_id=to_id, ref_ids=ref_ids)
    return _ok()


# attr/query/template/file/export/notification/system tools

def set_block_attrs(ctx: ToolContext, block_id: str, attrs: dict[str, Any]) -> dict[str, Any]:
    ctx.client.set_block_attrs(block_id, attrs)
    return _ok()


def get_block_attrs(ctx: ToolContext, block_id: str) -> dict[str, Any]:
    return {"attrs": ctx.client.get_block_attrs(block_id)}


def query_sql(ctx: ToolContext, stmt: str) -> dict[str, Any]:
    return {"rows": ctx.client.query_sql(stmt)}


def flush_transaction(ctx: ToolContext) -> dict[str, Any]:
    ctx.client.flush_transaction()
    return _ok()


def render_template(ctx: ToolContext, doc_id: str, path: str) -> dict[str, Any]:
    return {"data": ctx.client.render_template(doc_id, path)}


def render_sprig(ctx: ToolContext, template: str) -> dict[str, Any]:
    return {"result": ctx.client.render_sprig(template)}


def read_dir(ctx: ToolContext, path: str) -> dict[str, Any]:
    return {"entries": ctx.client.read_dir(path)}


def remove_file(ctx: ToolContext, path: str) -> dict[str, Any]:
    ctx.client.remove_file(path)
    return _ok()


def rename_file(ctx: ToolContext, path: str, new_path: str) -> dict[str, Any]:
    ctx.client.rename_file(path, new_path)
    return _ok()


def export_md_content(ctx: ToolContext, doc_id: str) -> dict[str, Any]:
    return {"data": ctx.client.export_md_content(doc_id)}


def export_resources(ctx: ToolContext, paths: list[str], name: str | None = None) -> dict[str, Any]:
    return {"data": ctx.client.export_resources(paths, name=name)}


def push_msg(ctx: ToolContext, msg: str, timeout: int | None = None) -> dict[str, Any]:
    return {"data": ctx.client.push_msg(msg, timeout=timeout)}


def push_err_msg(ctx: ToolContext, msg: str, timeout: int | None = None) -> dict[str, Any]:
    return {"data": ctx.client.push_err_msg(msg, timeout=timeout)}


def boot_progress(ctx: ToolContext) -> dict[str, Any]:
    return {"data": ctx.client.boot_progress()}


def system_version(ctx: ToolContext) -> dict[str, Any]:
    return {"version": ctx.client.version()}


def current_time(ctx: ToolContext) -> dict[str, Any]:
    return {"timestamp_ms": ctx.client.current_time()}


# backward compatibility for the initial scaffold

def create_document(
    ctx: ToolContext,
    notebook_id: str,
    doc_path: str,
    title: str,
    markdown: str,
) -> dict[str, Any]:
    doc_id = ctx.client.create_doc_with_md(notebook_id=notebook_id, path=doc_path, markdown=markdown)
    if title:
        ctx.client.rename_doc_by_id(doc_id=doc_id, title=title)
    return {"id": doc_id}


def search_documents(ctx: ToolContext, query: str, limit: int = 10) -> dict[str, Any]:
    safe_limit = max(1, int(limit))
    escaped = query.replace("'", "''")
    stmt = (
        "SELECT id, parent_id, root_id, hpath, content, markdown, type, updated "
        "FROM blocks "
        f"WHERE content LIKE '%{escaped}%' "
        "ORDER BY updated DESC "
        f"LIMIT {safe_limit}"
    )
    return {"rows": ctx.client.query_sql(stmt), "stmt": stmt}


TOOL_REGISTRY: dict[str, ToolFunc] = {
    "call_api": call_api,
    "list_notebooks": list_notebooks,
    "open_notebook": open_notebook,
    "close_notebook": close_notebook,
    "create_notebook": create_notebook,
    "rename_notebook": rename_notebook,
    "remove_notebook": remove_notebook,
    "get_notebook_conf": get_notebook_conf,
    "set_notebook_conf": set_notebook_conf,
    "create_doc_with_md": create_doc_with_md,
    "rename_doc": rename_doc,
    "rename_doc_by_id": rename_doc_by_id,
    "remove_doc": remove_doc,
    "remove_doc_by_id": remove_doc_by_id,
    "move_docs": move_docs,
    "move_docs_by_id": move_docs_by_id,
    "get_hpath_by_path": get_hpath_by_path,
    "get_hpath_by_id": get_hpath_by_id,
    "get_path_by_id": get_path_by_id,
    "get_ids_by_hpath": get_ids_by_hpath,
    "insert_block": insert_block,
    "prepend_block": prepend_block,
    "append_block": append_block,
    "update_block": update_block,
    "delete_block": delete_block,
    "move_block": move_block,
    "fold_block": fold_block,
    "unfold_block": unfold_block,
    "get_block_kramdown": get_block_kramdown,
    "get_child_blocks": get_child_blocks,
    "transfer_block_ref": transfer_block_ref,
    "set_block_attrs": set_block_attrs,
    "get_block_attrs": get_block_attrs,
    "query_sql": query_sql,
    "flush_transaction": flush_transaction,
    "render_template": render_template,
    "render_sprig": render_sprig,
    "read_dir": read_dir,
    "remove_file": remove_file,
    "rename_file": rename_file,
    "export_md_content": export_md_content,
    "export_resources": export_resources,
    "push_msg": push_msg,
    "push_err_msg": push_err_msg,
    "boot_progress": boot_progress,
    "system_version": system_version,
    "current_time": current_time,
    "create_document": create_document,
    "search_documents": search_documents,
}


def list_tools() -> list[str]:
    return sorted(TOOL_REGISTRY.keys())


def run_tool(ctx: ToolContext, tool_name: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
    if tool_name not in TOOL_REGISTRY:
        raise KeyError(f"Unknown tool: {tool_name}")

    payload = args or {}
    return TOOL_REGISTRY[tool_name](ctx, **payload)
