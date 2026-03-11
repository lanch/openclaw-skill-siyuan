---
name: openclaw-siyuan
description: Integrate OpenClaw with SiYuan's official HTTP API for notebook management, document/filetree operations, block editing, attributes, SQL querying, export, notifications, and system status. Use when tasks involve reading or writing SiYuan content, automating note workflows, or troubleshooting SiYuan API calls.
---

# OpenClaw SiYuan Skill

Use this skill to execute SiYuan API workflows through tool calls.

## Follow the API source of truth

- API source: `https://raw.githubusercontent.com/siyuan-note/siyuan/refs/heads/master/API_zh_CN.md`
- Treat endpoint path and payload fields as authoritative from that document.
- Prefer dedicated tools first; use `call_api` for endpoints not yet wrapped.

## Configure before calling tools

- `SIYUAN_BASE_URL` default: `http://127.0.0.1:6806`
- `SIYUAN_TOKEN` default: empty
- `SIYUAN_TIMEOUT` default: `10`

## Use the right tool category

- Notebook: `list_notebooks`, `open_notebook`, `close_notebook`, `create_notebook`, `rename_notebook`, `remove_notebook`, `get_notebook_conf`, `set_notebook_conf`
- Filetree/doc: `create_doc_with_md`, `rename_doc`, `rename_doc_by_id`, `remove_doc`, `remove_doc_by_id`, `move_docs`, `move_docs_by_id`, `get_hpath_by_path`, `get_hpath_by_id`, `get_path_by_id`, `get_ids_by_hpath`
- Block: `insert_block`, `prepend_block`, `append_block`, `update_block`, `delete_block`, `move_block`, `fold_block`, `unfold_block`, `get_block_kramdown`, `get_child_blocks`, `transfer_block_ref`
- Attr/SQL/template: `set_block_attrs`, `get_block_attrs`, `query_sql`, `flush_transaction`, `render_template`, `render_sprig`
- File/export/notify/system: `read_dir`, `remove_file`, `rename_file`, `export_md_content`, `export_resources`, `push_msg`, `push_err_msg`, `boot_progress`, `system_version`, `current_time`
- Generic fallback: `call_api`

## Apply these workflow rules

1. Resolve target IDs before mutation.
2. Prefer `*_by_id` endpoints when available.
3. For block insertions, pass at least one anchor (`next_id`, `previous_id`, `parent_id`).
4. For custom attributes, use keys prefixed with `custom-`.
5. Escape single quotes in SQL LIKE strings (`'` -> `''`) before calling `query_sql`.

## Handle compatibility tools

- `create_document`: legacy alias that creates document markdown then renames by ID when `title` is provided.
- `search_documents`: legacy alias that performs SQL search on `blocks` table.

## Run local checks

```bash
python -m compileall src tests
```
