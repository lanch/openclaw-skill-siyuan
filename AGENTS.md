# Agent Notes

## Project goal

Provide a clean, testable Python structure for SiYuan integration in OpenClaw.

## Code boundaries

- `config.py`: configuration and environment parsing only.
- `client.py`: HTTP request logic and API error handling.
- `tools.py`: tool-level wrappers and dispatch registry.
- `server.py`: request handling and CLI entrypoint.

## Commands

- Install (editable): `pip install -e .[dev]`
- Test: `pytest`
