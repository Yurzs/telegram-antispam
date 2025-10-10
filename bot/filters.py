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

    links = []

    # Pattern to match URLs with protocol
    url_with_protocol = r'https?://[^\s<>"{}|\\^`\[\]]+'

    # Pattern to match URLs without protocol (common short links and domains)
    # Matches things like: t.co/xyz, bit.ly/abc, example.com/path
    url_without_protocol = r"(?:^|[\s])([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(?:\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(?:/[^\s]*)?)"

    # Pattern to match @username mentions
    mention_pattern = r"@[\w]+"

    # Pattern to match t.me links (with or without protocol)
    tme_pattern = r"(?:https?://)?t\.me/[^\s]+"

    # Extract URLs with protocol
    links.extend(re.findall(url_with_protocol, text, re.IGNORECASE))

    # Extract URLs without protocol
    for match in re.finditer(url_without_protocol, text, re.IGNORECASE):
        url = match.group(1).strip()
        # Only add if it looks like a real URL (has a path or known short domain)
        if "/" in url or any(
            domain in url.lower()
            for domain in ["t.co", "bit.ly", "tinyurl.com", "goo.gl"]
        ):
            links.append(url)

    # Extract @mentions
    links.extend(re.findall(mention_pattern, text, re.IGNORECASE))

    # Extract t.me links (may overlap but that's ok)
    links.extend(re.findall(tme_pattern, text, re.IGNORECASE))

    # Remove duplicates while preserving order
    seen = set()
    unique_links = []
    for link in links:
        if link.lower() not in seen:
            seen.add(link.lower())
            unique_links.append(link)

    return unique_links


def extract_entities_links(message: Message) -> list[str]:
    """Extract links from message entities (formatted links in HTML/Markdown)."""
    links = []

    if not message.entities:
        return links

    for entity in message.entities:
        # Check for URL entities
        if entity.type == "url":
            # Extract the URL text from the message
            if message.text:
                url = message.text[entity.offset : entity.offset + entity.length]
                links.append(url)
        # Check for text_link entities (formatted links like [text](url))
        elif entity.type == "text_link" and entity.url:
            links.append(entity.url)

    return links


async def get_linked_channel(bot: Bot, chat_id: int) -> Optional[Chat]:
    """Get the channel linked to a chat (discussion group)."""
    try:
        chat = await bot.get_chat(chat_id)
        # Check if this chat has a linked chat (for discussion groups, this is the channel)
        if hasattr(chat, "linked_chat_id") and chat.linked_chat_id:
            linked_chat = await bot.get_chat(chat.linked_chat_id)
            return linked_chat
    except Exception as e:
        # Log the error for debugging
        import logging

        logging.getLogger(__name__).error(
            f"Error getting linked channel for chat {chat_id}: {e}"
        )
    return None


def is_link_to_channel(
    link: str,
    channel_username: Optional[str] = None,
    channel_id: Optional[int] = None,
    chat_id: Optional[int] = None,
) -> bool:
    """Check if link points to the allowed channel or current chat.

    Args:
        link: The link to check
        channel_username: Username of the allowed channel
        channel_id: ID of the linked channel
        chat_id: ID of the current chat

    Returns:
        True if link is to allowed channel or current chat, False otherwise
    """
    # Check username-based links
    if channel_username:
        # Remove @ if present
        clean_username = channel_username.lstrip("@")

        # Check various formats
        patterns = [
            f"@{clean_username}",
            f"t.me/{clean_username}",
            f"https://t.me/{clean_username}",
            f"http://t.me/{clean_username}",
        ]

        if any(pattern.lower() in link.lower() for pattern in patterns):
            return True

    # Check t.me/c/{channel_id} format (private channel/group links)
    # Format: t.me/c/2929399460/7 or https://t.me/c/2929399460/7
    # The ID in URL is without -100 prefix
    import re

    tme_c_pattern = r"t\.me/c/(\d+)(?:/\d+)?"
    match = re.search(tme_c_pattern, link, re.IGNORECASE)

    if match:
        link_channel_id = int(match.group(1))

        # Check if it matches the linked channel
        if channel_id:
            # Channel IDs in Telegram API have -100 prefix for supergroups/channels
            # The link format uses ID without -100 prefix
            channel_id_without_prefix = abs(channel_id) % 10000000000
            if link_channel_id == channel_id_without_prefix:
                return True

        # Check if it matches the current chat
        if chat_id:
            chat_id_without_prefix = abs(chat_id) % 10000000000
            if link_channel_id == chat_id_without_prefix:
                return True

    return False


async def should_delete_message(
    bot: Bot,
    message: Message,
    allowed_channel_username: Optional[str] = None,
    linked_channel_id: Optional[int] = None,
) -> bool:
    """Determine if message should be deleted based on filtering rules.

    Args:
        bot: Bot instance
        message: Message to check
        allowed_channel_username: Username of the channel that is allowed
        linked_channel_id: ID of the linked channel

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

    # Extract all links from text
    links = extract_links(text)

    # Also extract links from message entities (formatted links)
    entity_links = extract_entities_links(message)
    links.extend(entity_links)

    # No links found - message is OK
    if not links:
        return False

    # Get current chat ID
    chat_id = message.chat.id if message.chat else None

    # Check each link
    for link in links:
        # If link is to the allowed channel or current chat, it's OK
        if is_link_to_channel(
            link, allowed_channel_username, linked_channel_id, chat_id
        ):
            continue
        # Found a link that's not to the allowed channel or current chat
        return True

    # All links are to the allowed channel or current chat
    return False
