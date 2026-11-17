
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN, DATABASE_URL
from bot.handlers import router
from bot.memory import Memory


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties()
    )

    memory = Memory(DATABASE_URL)

    try:
        await memory.connect()

        dp = Dispatcher()
        dp["memory"] = memory

        dp.include_router(router)

        await bot.delete_webhook(drop_pending_updates=True)

        logging.info("Premium Claude Telegram bot started")

        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )

    finally:
        await memory.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
