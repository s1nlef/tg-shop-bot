from aiogram.types import ErrorEvent
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers.purchase import purchase
from app.handlers.catalog import catalog
from app.handlers.admin import admin
import asyncio
import logging
import os


async def error_handler(event: ErrorEvent):
    logging.error(
        f"Update: {event.update.update_id} caused error: {event.exception}",
        exc_info=True,
    )
    if event.update.message:
        try:
            await event.update.message.answer(
                "⚠️ An error occurred. Please try again later or contact the administrator."
            )
        except Exception:
            pass


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.error.register(error_handler)
    dp.include_routers(purchase, catalog, admin)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped🛑")
