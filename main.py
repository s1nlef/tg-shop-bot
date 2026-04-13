import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers.user import user
from app.handlers.admin import admin
from app.database.models import async_main


async def main():
    load_dotenv()
    await async_main()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(user, admin)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stoped🛑")