import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import load_config
from bot.database import Database
from bot.handlers import setup_routers
from bot.logging_config import setup_logging
from bot.middlewares.db import DatabaseMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    config = load_config()
    setup_logging(config.log_level)

    db = Database(config.database_url)
    await db.init_models()

    bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp["config"] = config
    dp.update.outer_middleware(ThrottlingMiddleware(config.rate_limit_seconds))
    dp.update.outer_middleware(DatabaseMiddleware(db))

    dp.include_router(setup_routers())

    logger.info("Starting TaskFlow bot")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
