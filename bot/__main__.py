"""Telegram Antispam Bot - Main module."""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import Config
from .handlers import router


def setup_logging(log_level: str) -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


async def main() -> None:
    """Main bot function."""
    # Load configuration
    config = Config.from_env()
    
    # Setup logging
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Telegram Antispam Bot...")
    
    # Initialize bot and dispatcher
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    
    # Register router
    dp.include_router(router)
    
    # Start polling
    try:
        logger.info("Bot started successfully!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
