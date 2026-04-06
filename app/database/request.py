from app.database.models import async_session
from app.database.models import User, Game, CartItem
from sqlalchemy import select, delete

# Поиск/вывод данных
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id,))
            await session.commit()      

async def check_balance(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.balance
        

async def get_all_games():
    async with async_session() as session:
        return (await session.scalars(select(Game))).all()
    
async def get_game(game_id):
    async with async_session() as session:
        return await session.scalar(select(Game).where(Game.id == game_id))
    
# Изменения данных
  
async def add_to_cart(tg_id, game_id):
    async with async_session() as session:
        session.add(CartItem(tg_id=tg_id, game_id=game_id))
        await session.commit()
        return  

async def get_cart(tg_id):
    async with async_session() as session:
        cart = (await session.scalar(select(CartItem).where(tg_id=tg_id))).all()
        return cart.game_id
    
async def remove_from_cart(tg_id, game_id):
    async with async_session() as session:
        await session.execute(delete(CartItem).where(CartItem.tg_id == tg_id, CartItem.game_id == game_id))
        await session.commit()
        return
    
async def clean_cart(tg_id):
    async with async_session() as session:
        await session.delete(select(CartItem).where(tg_id=tg_id))
        await session.commit()
        return