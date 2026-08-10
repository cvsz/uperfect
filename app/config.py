"""Runtime configuration that deliberately keeps secret values private."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, repr=False)
class Settings:
    """Configuration loaded only from the process environment."""

    database_path: str
    line_channel_access_token: str | None

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            database_path=os.getenv("UPERFECT_DATABASE_PATH", "uperfect.db"),
            line_channel_access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN") or None,
        )

    def integration_status(self, name: str) -> str:
        if name == "line" and self.line_channel_access_token:
            return "configured"
        return "unconfigured"

