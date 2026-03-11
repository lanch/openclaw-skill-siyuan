---
name: openclaw-siyuan
description: Integrate with the SiYuan HTTP API for notebook listing, document creation, and full-text search. Use when implementing or debugging OpenClaw tool workflows that read or write SiYuan content.
---

# OpenClaw SiYuan Skill

## Keep responsibilities clear

- Keep API details in `src/openclaw_skill_siyuan/client.py`.
- Keep environment loading in `src/openclaw_skill_siyuan/config.py`.
- Keep user-facing tool contracts in `src/openclaw_skill_siyuan/tools.py`.
- Keep transport/CLI entrypoint logic in `src/openclaw_skill_siyuan/server.py`.

## Run locally

```bash
python -m pytest
```

## Environment variables

- `SIYUAN_BASE_URL` (default: `http://127.0.0.1:6806`)
- `SIYUAN_TOKEN` (default: empty)
- `SIYUAN_TIMEOUT` (default: `10`)
