# openclaw-skill-siyuan

基于思源笔记官方 HTTP API 的 OpenClaw skill 实现。

官方 API 文档：<https://raw.githubusercontent.com/siyuan-note/siyuan/refs/heads/master/API_zh_CN.md>

## 项目结构

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
│  ├─ test_server.py
│  └─ test_tools.py
└─ README.md
```

## 安装

```bash
pip install -e .[dev]
```

## 环境变量

- `SIYUAN_BASE_URL`，默认 `http://127.0.0.1:6806`
- `SIYUAN_TOKEN`，默认空
- `SIYUAN_TIMEOUT`，默认 `10`

## 列出可用工具

```bash
python -m openclaw_skill_siyuan.server --list-tools
```

## 调用示例

```bash
python -m openclaw_skill_siyuan.server --request '{"tool":"list_notebooks","args":{}}'
```

```bash
python -m openclaw_skill_siyuan.server --request '{"tool":"create_doc_with_md","args":{"notebook_id":"20210817205410-2kvfpfn","path":"/demo/note","markdown":"# hello"}}'
```

## 覆盖范围

已封装官方 API 的常用端点：笔记本、文档/文件树、块操作、属性、SQL、模板、文件目录、导出、通知、系统状态。

对未封装或新增端点可用 `call_api` 直接调用。
