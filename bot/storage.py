"""Telegram Antispam Bot - Storage module."""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ChatConfig:
    """Configuration for a specific chat."""

    chat_id: int
    enabled: bool = True
    allowed_channel_username: Optional[str] = None


# In-memory storage for chat configurations
# In production, this should be replaced with a database
_chat_configs: Dict[int, ChatConfig] = {}


def get_chat_config(chat_id: int) -> ChatConfig:
    """Get configuration for a chat."""
    if chat_id not in _chat_configs:
        _chat_configs[chat_id] = ChatConfig(chat_id=chat_id)
    return _chat_configs[chat_id]


def set_chat_config(chat_id: int, config: ChatConfig) -> None:
    """Set configuration for a chat."""
    _chat_configs[chat_id] = config
