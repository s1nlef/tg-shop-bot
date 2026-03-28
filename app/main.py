import asyncio
import logging
import os
import sqlite3
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers.handlers import user

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)

def db_init() -> None:
    try:
        conection = sqlite3.connect("tg-shop.db")
        cursor = conection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS games (id PRIMERY KEY, name TEXT NOT NULL, steamlink TEXT NOT NULL, daterelease TEXT NOT NULL)")
    except:
        conection.commit()
        conection.close()
    finally:
        conection.commit()
        conection.close()
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        db_init()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stoped🛑")