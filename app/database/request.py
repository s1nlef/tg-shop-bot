from app.database.models import async_session
from app.database.models import User, Game, CartItem, Order, OrderItem
from sqlalchemy import select, delete, update
from app.handlers.admin import ADMINS_TG_ID
import asyncio

# Поиск/вывод данных
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id,))
            await session.commit()      

async def check_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))

        

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
        cart = (await session.scalars(select(CartItem).where(CartItem.tg_id==tg_id))).all()
        return cart
    
async def remove_from_cart(tg_id, game_id):
    async with async_session() as session:
        await session.execute(delete(CartItem).where(CartItem.tg_id == tg_id, CartItem.game_id == game_id))
        await session.commit()
        return
    
async def clean_cart(tg_id):
    async with async_session() as session:
        await session.execute(delete(CartItem).where(CartItem.tg_id == tg_id))
        await session.commit()
        return

async def admin_change_balance(balance):
    async with async_session() as session:
        admin = await session.scalar(select(User).where(User.tg_id == ADMINS_TG_ID))
        admin.balance = balance
        await session.commit()
        return

async def change_balance(tg_id, total_sum):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.balance -= total_sum
        await session.commit()
        return

async def create_order(tg_id):
    async with async_session() as session:
        cart = await get_cart(tg_id=tg_id)
        games = await asyncio.gather(*(get_game(item.game_id) for item in cart))
            
        sum_price = sum([game.price for game in games])

        order = Order(tg_id=tg_id, price=sum_price)
        session.add(order)
        await session.flush()
        for  game in games:
            session.add(OrderItem(
                order_id=order.id,
                game_id=game.id,
                price=game.price
            ))
        await session.commit()
        return order.id

async def all_user_orders(tg_id):
    async with async_session() as session:
        return (await session.scalars(select(Order).where(Order.tg_id == tg_id).order_by(Order.created_at.desc()))).all()


async def get_order_items(order_id):
    async with async_session() as session:
        return (await session.scalars(select(OrderItem).where(OrderItem.order_id == order_id))).all()