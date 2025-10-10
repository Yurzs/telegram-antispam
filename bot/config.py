"""Telegram Antispam Bot - Configuration module."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Bot configuration."""

    bot_token: str
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            raise ValueError("BOT_TOKEN environment variable is required")

        return cls(
            bot_token=bot_token,
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
