"""Telegram Antispam Bot - Handlers module."""

import logging

from aiogram import Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from .filters import is_user_admin, get_linked_channel, should_delete_message
from .storage import ChatConfig, get_chat_config, set_chat_config

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot) -> None:
    """Handle /start command."""
    if not message.from_user or not message.chat:
        return
    
    # Check if user is admin in this chat
    is_admin = await is_user_admin(bot, message.chat.id, message.from_user.id)
    
    if message.chat.type == "private":
        await message.answer(
            "👋 Welcome to Telegram Antispam Bot!\n\n"
            "This bot helps filter spam messages in channel discussion groups.\n\n"
            "To use this bot:\n"
            "1. Add the bot to your channel's discussion group\n"
            "2. Make the bot an admin with 'Delete messages' permission\n"
            "3. Use /status in the group to get the chat ID\n"
            "4. Use /config <chat_id> here in private chat to configure the bot\n"
        )
    elif is_admin:
        await message.answer(
            "✅ Bot is ready!\n\n"
            "I will automatically filter messages with links from non-admin users.\n"
            "Links to your connected channel are allowed.\n\n"
            f"Use /status to check bot status and get the chat ID.\n"
            f"Use `/config {message.chat.id}` in private chat with the bot to configure settings."
        )
    else:
        await message.answer("❌ This command is only available to admins.")


@router.message(Command("config"))
async def cmd_config(message: Message, bot: Bot) -> None:
    """Handle /config command with chat ID parameter in private messages."""
    if not message.from_user or not message.chat:
        return
    
    # Only work in private messages
    if message.chat.type != "private":
        await message.answer(
            "⚠️ This command only works in private messages.\n"
            "Use /config <chat_id> to configure a specific chat."
        )
        return
    
    # Parse chat ID from command arguments
    command_args = message.text.split(maxsplit=1) if message.text else []
    if len(command_args) < 2:
        await message.answer(
            "❌ Please provide a chat ID.\n\n"
            "Usage: /config <chat_id>\n"
            "Example: /config -1002986805684\n\n"
            "You can get the chat ID by using /status in the group."
        )
        return
    
    try:
        chat_id = int(command_args[1])
    except ValueError:
        await message.answer("❌ Invalid chat ID. Please provide a valid numeric chat ID.")
        return
    
    # Check if user is admin in the specified chat
    is_admin = await is_user_admin(bot, chat_id, message.from_user.id)
    if not is_admin:
        await message.answer(
            f"❌ You are not an admin in chat {chat_id}.\n"
            "You can only configure chats where you are an admin."
        )
        return
    
    # Get current config
    config = get_chat_config(chat_id)
    
    # Get linked channel info
    linked_channel = await get_linked_channel(bot, chat_id)
    
    config_text = "⚙️ Current Configuration:\n\n"
    config_text += f"Chat ID: {chat_id}\n"
    config_text += f"Enabled: {'✅ Yes' if config.enabled else '❌ No'}\n"
    
    if linked_channel:
        config_text += f"Linked Channel: @{linked_channel.username or 'N/A'} ({linked_channel.title})\n"
        # Auto-update allowed channel if linked channel exists
        if linked_channel.username:
            config.allowed_channel_username = linked_channel.username
            set_chat_config(chat_id, config)
    else:
        config_text += "Linked Channel: None\n"
    
    config_text += f"Allowed Channel: @{config.allowed_channel_username or 'N/A'}\n"
    
    config_text += "\n💡 The bot automatically detects the linked channel and allows links to it."
    
    await message.answer(config_text)


@router.message(Command("status"))
async def cmd_status(message: Message, bot: Bot) -> None:
    """Handle /status command."""
    if not message.from_user or not message.chat:
        return
    
    # Only work in groups
    if message.chat.type == "private":
        await message.answer("⚠️ This command only works in groups.")
        return
    
    # Check if user is admin
    is_admin = await is_user_admin(bot, message.chat.id, message.from_user.id)
    if not is_admin:
        await message.answer("❌ This command is only available to admins.")
        return
    
    # Check bot permissions
    try:
        bot_member = await bot.get_chat_member(message.chat.id, bot.id)
        can_delete = bot_member.can_delete_messages if hasattr(bot_member, 'can_delete_messages') else False
    except Exception:
        can_delete = False
    
    config = get_chat_config(message.chat.id)
    linked_channel = await get_linked_channel(bot, message.chat.id)
    
    status_text = "📊 Bot Status:\n\n"
    status_text += f"Chat ID: `{message.chat.id}`\n"
    status_text += f"Filtering: {'✅ Active' if config.enabled else '❌ Inactive'}\n"
    status_text += f"Can Delete Messages: {'✅ Yes' if can_delete else '❌ No'}\n"
    
    if linked_channel:
        status_text += f"Monitoring: {linked_channel.title}\n"
    
    if not can_delete:
        status_text += "\n⚠️ Warning: Bot doesn't have permission to delete messages. Please make the bot an admin with 'Delete messages' permission."
    
    status_text += f"\n\n💡 Use `/config {message.chat.id}` in private chat with the bot to configure settings."
    
    await message.answer(status_text, parse_mode="Markdown")


@router.message(Command("enable"))
async def cmd_enable(message: Message, bot: Bot) -> None:
    """Handle /enable command."""
    if not message.from_user or not message.chat:
        return
    
    if message.chat.type == "private":
        await message.answer("⚠️ This command only works in groups.")
        return
    
    is_admin = await is_user_admin(bot, message.chat.id, message.from_user.id)
    if not is_admin:
        await message.answer("❌ This command is only available to admins.")
        return
    
    config = get_chat_config(message.chat.id)
    config.enabled = True
    set_chat_config(message.chat.id, config)
    
    await message.answer("✅ Spam filtering enabled!")


@router.message(Command("disable"))
async def cmd_disable(message: Message, bot: Bot) -> None:
    """Handle /disable command."""
    if not message.from_user or not message.chat:
        return
    
    if message.chat.type == "private":
        await message.answer("⚠️ This command only works in groups.")
        return
    
    is_admin = await is_user_admin(bot, message.chat.id, message.from_user.id)
    if not is_admin:
        await message.answer("❌ This command is only available to admins.")
        return
    
    config = get_chat_config(message.chat.id)
    config.enabled = False
    set_chat_config(message.chat.id, config)
    
    await message.answer("❌ Spam filtering disabled!")


@router.message()
async def filter_message(message: Message, bot: Bot) -> None:
    """Filter messages for spam."""
    if not message.chat:
        return
    
    # Only filter in groups/supergroups
    if message.chat.type == "private":
        return
    
    # Get chat config
    config = get_chat_config(message.chat.id)
    
    # Skip if filtering is disabled
    if not config.enabled:
        return
    
    # Get linked channel and update config
    linked_channel = await get_linked_channel(bot, message.chat.id)
    if linked_channel and linked_channel.username:
        config.allowed_channel_username = linked_channel.username
        set_chat_config(message.chat.id, config)
    
    # Check if message is from the linked channel (sender_chat field)
    # Messages from channels have from.id = 777000 and sender_chat contains the actual channel
    if message.sender_chat and linked_channel:
        if message.sender_chat.id == linked_channel.id:
            # This is a message from the linked channel, don't filter it
            logger.debug(
                f"Skipping message from linked channel {linked_channel.id} in chat {message.chat.id}"
            )
            return
    
    # Skip if no from_user (shouldn't happen after sender_chat check, but be safe)
    if not message.from_user:
        return
    
    # Check if message should be deleted
    try:
        if await should_delete_message(bot, message, config.allowed_channel_username):
            await message.delete()
            logger.info(
                f"Deleted message from user {message.from_user.id} in chat {message.chat.id}"
            )
            
            # Optionally notify the user (can be removed if too noisy)
            # await message.answer(
            #     f"⚠️ Message from {message.from_user.mention_html()} was deleted (external links not allowed)",
            #     parse_mode="HTML"
            # )
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")
