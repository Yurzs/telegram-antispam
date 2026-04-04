"""Telegram Antispam Bot - Configuration module."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Bot configuration."""

    bot_token: str
    log_level: str = "INFO"
    webhook_mode: bool = False
    webhook_host: str = ""
    webhook_path: str = "/webhook"
    webhook_port: int = 8080
    webhook_secret: str = ""
    proxy_url: str = ""

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            raise ValueError("BOT_TOKEN environment variable is required")

        webhook_mode = os.getenv("WEBHOOK_MODE", "false").lower() == "true"
        
        # Validate webhook configuration if webhook mode is enabled
        webhook_host = os.getenv("WEBHOOK_HOST", "")
        if webhook_mode and not webhook_host:
            raise ValueError("WEBHOOK_HOST is required when WEBHOOK_MODE is true")

        return cls(
            bot_token=bot_token,
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            webhook_mode=webhook_mode,
            webhook_host=webhook_host,
            webhook_path=os.getenv("WEBHOOK_PATH", "/webhook"),
            webhook_port=int(os.getenv("WEBHOOK_PORT", "8080")),
            webhook_secret=os.getenv("WEBHOOK_SECRET", ""),
            proxy_url=os.getenv("PROXY_URL", ""),
        )
