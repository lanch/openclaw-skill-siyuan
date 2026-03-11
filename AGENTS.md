# Agent Notes

## Project goal

Provide a clean, testable Python structure for SiYuan integration in OpenClaw.

## Tech stack
- Python 3.11
- httpx
- hatchling
- pytest

## Code boundaries

- `config.py`: configuration and environment parsing only.
- `client.py`: HTTP request logic and API error handling.
- `tools.py`: tool-level wrappers and dispatch registry.
- `server.py`: request handling and CLI entrypoint.

## Coding rules
- Prefer small modules and clear names
- Add type hints everywhere
- Wrap SiYuan HTTP API in a dedicated client
- Do not hardcode token or host
- Keep functions pure where possible
- Add docstrings for public APIs

## Testing
- Use pytest
- Mock external HTTP requests
- Add at least one happy-path and one error-path test per public tool

## Commands

- Install (editable): `pip install -e .[dev]`
- Test: `python -m pytest`
