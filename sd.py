from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgresql:Superparol@localhost:5432/tg_shop"

async def test():
    engine = create_async_engine(DATABASE_URL)
    async with engine.connect() as conn:
        print("OK")
    await engine.dispose()

asyncio.run(test())