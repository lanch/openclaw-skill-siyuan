# openclaw-skill-siyuan

A minimal Python scaffold for integrating OpenClaw tools with the SiYuan HTTP API.

## Project layout

```text
openclaw-skill-siyuan/
├─ SKILL.md
├─ AGENTS.md
├─ pyproject.toml
├─ src/
│  └─ openclaw_skill_siyuan/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ client.py
│     ├─ tools.py
│     └─ server.py
├─ tests/
│  ├─ test_client.py
│  └─ test_tools.py
└─ README.md
```

## Install

```bash
pip install -e .[dev]
```

## Run tests

```bash
pytest
```

## Example request

```bash
python -m openclaw_skill_siyuan.server --request '{"tool":"list_notebooks","args":{}}'
```

## Environment

- `SIYUAN_BASE_URL` default: `http://127.0.0.1:6806`
- `SIYUAN_TOKEN` default: empty
- `SIYUAN_TIMEOUT` default: `10`
