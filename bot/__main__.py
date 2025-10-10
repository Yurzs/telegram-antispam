"""Telegram Antispam Bot - Main module."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

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

    if config.webhook_mode:
        # Webhook mode
        logger.info("Running in webhook mode")
        
        # Set webhook
        webhook_url = f"{config.webhook_host}{config.webhook_path}"
        logger.info(f"Setting webhook to {webhook_url}")
        
        await bot.set_webhook(
            url=webhook_url,
            secret_token=config.webhook_secret if config.webhook_secret else None,
            drop_pending_updates=True,
        )
        
        # Create aiohttp application
        app = web.Application()
        
        # Create webhook request handler
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=config.webhook_secret if config.webhook_secret else None,
        )
        
        # Register webhook handler on the specified path
        webhook_requests_handler.register(app, path=config.webhook_path)
        
        # Setup the application
        setup_application(app, dp, bot=bot)
        
        # Start the web server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=config.webhook_port)
        
        try:
            await site.start()
            logger.info(f"Webhook server started on port {config.webhook_port}")
            logger.info("Bot started successfully!")
            
            # Keep the application running
            await asyncio.Event().wait()
        finally:
            await bot.delete_webhook(drop_pending_updates=True)
            await runner.cleanup()
            await bot.session.close()
    else:
        # Polling mode
        logger.info("Running in polling mode")
        
        # Delete webhook if it was set before
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Start polling
        try:
            logger.info("Bot started successfully!")
            await dp.start_polling(bot)
        finally:
            await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
