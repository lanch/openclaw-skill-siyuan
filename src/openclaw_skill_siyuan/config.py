"""Configuration helpers for SiYuan integration."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SiyuanConfig:
    """Runtime configuration for the SiYuan API client."""

    base_url: str = "http://127.0.0.1:6806"
    token: str = ""
    timeout: float = 10.0

    @classmethod
    def from_env(cls) -> "SiyuanConfig":
        timeout_raw = os.getenv("SIYUAN_TIMEOUT", str(cls.timeout))
        try:
            timeout = float(timeout_raw)
        except ValueError:
            timeout = cls.timeout

        return cls(
            base_url=os.getenv("SIYUAN_BASE_URL", cls.base_url),
            token=os.getenv("SIYUAN_TOKEN", cls.token),
            timeout=timeout,
        )

    def auth_headers(self) -> dict[str, str]:
        if not self.token:
            return {}
        return {"Authorization": f"Token {self.token}"}
