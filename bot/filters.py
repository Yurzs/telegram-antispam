"""Telegram Antispam Bot - Filters module."""

import re
from typing import Optional

from aiogram import Bot
from aiogram.types import Message, Chat


async def is_user_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """Check if user is an admin in the chat."""
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ["creator", "administrator"]
    except Exception:
        return False


def extract_links(text: Optional[str]) -> list[str]:
    """Extract all links from text."""
    if not text:
        return []
    
    # Pattern to match URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    # Pattern to match @username mentions
    mention_pattern = r'@[\w]+'
    # Pattern to match t.me links
    tme_pattern = r't\.me/[\w]+'
    
    urls = re.findall(url_pattern, text, re.IGNORECASE)
    mentions = re.findall(mention_pattern, text, re.IGNORECASE)
    tme_links = re.findall(tme_pattern, text, re.IGNORECASE)
    
    return urls + mentions + tme_links


async def get_linked_channel(bot: Bot, chat_id: int) -> Optional[Chat]:
    """Get the channel linked to a chat (discussion group)."""
    try:
        chat = await bot.get_chat(chat_id)
        if chat.linked_chat_id:
            linked_chat = await bot.get_chat(chat.linked_chat_id)
            return linked_chat
    except Exception:
        pass
    return None


def is_link_to_channel(link: str, channel_username: Optional[str]) -> bool:
    """Check if link points to the allowed channel."""
    if not channel_username:
        return False
    
    # Remove @ if present
    channel_username = channel_username.lstrip("@")
    
    # Check various formats
    patterns = [
        f"@{channel_username}",
        f"t.me/{channel_username}",
        f"https://t.me/{channel_username}",
        f"http://t.me/{channel_username}",
    ]
    
    return any(pattern.lower() in link.lower() for pattern in patterns)


async def should_delete_message(
    bot: Bot,
    message: Message,
    allowed_channel_username: Optional[str] = None
) -> bool:
    """Determine if message should be deleted based on filtering rules.
    
    Args:
        bot: Bot instance
        message: Message to check
        allowed_channel_username: Username of the channel that is allowed
        
    Returns:
        True if message should be deleted, False otherwise
    """
    # Skip if message has no text
    if not message.text and not message.caption:
        return False
    
    text = message.text or message.caption or ""
    
    # Check if user is admin
    if message.from_user and message.chat:
        is_admin = await is_user_admin(bot, message.chat.id, message.from_user.id)
        if is_admin:
            return False
    
    # Extract all links
    links = extract_links(text)
    
    # No links found - message is OK
    if not links:
        return False
    
    # Check each link
    for link in links:
        # If link is to the allowed channel, it's OK
        if allowed_channel_username and is_link_to_channel(link, allowed_channel_username):
            continue
        # Found a link that's not to the allowed channel
        return True
    
    # All links are to the allowed channel
    return False
