from app.database.models import async_session
from app.database.models import User, Game, CartItem, Order, OrderItem
from sqlalchemy import select, delete, update
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

async def get_all_games(page: int, per_page: int = 5):
    async with async_session() as session:
        return (await session.scalars(select(Game).limit(per_page).offset(page * per_page))).all()
    
async def get_game(game_id: int):
    async with async_session() as session:
        return await session.scalar(select(Game).where(Game.id == game_id))
    
async def get_games_by_ids(game_ids: list[int]):
    async with async_session() as session:
        return (await session.scalars(select(Game).where(Game.id.in_(game_ids)))).all()

async def add_to_cart(tg_id, game_id):
    async with async_session() as session:
        cart = await session.scalar(select(CartItem).where(CartItem.tg_id == tg_id, CartItem.game_id == game_id))
        if cart:
            cart.quantity += 1
        else:
            session.add(CartItem(tg_id=tg_id, game_id=game_id))
        await session.commit()
        return  

async def get_cart(tg_id):
    async with async_session() as session:
        return (await session.scalars(select(CartItem).where(CartItem.tg_id==tg_id))).all()
    
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

async def admin_change_balance(tg_id, balance):
    async with async_session() as session:
        admin = await session.scalar(select(User).where(User.tg_id == tg_id))
        admin.balance = balance
        await session.commit()
        return

async def change_balance(tg_id, total_sum):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.balance -= total_sum
        await session.commit()
        return


async def create_order(tg_id, order_table):
    async with async_session() as session:
        
        print(order_table)
        order = Order(tg_id = tg_id, price = order_table["total"])
        session.add(order)
        await session.flush()
        for game, qty in zip(order_table["game"], order_table["quantity"]):
            session.add(OrderItem(
                order_id = order.id,
                game_id = game.id,
                quantity = qty,
                price = game.price*qty
            ))
        await session.commit()
        return order.id

async def all_user_orders(tg_id):
    async with async_session() as session:
        return (await session.scalars(select(Order).where(Order.tg_id == tg_id).order_by(Order.created_at.desc()))).all()


async def get_order_items(order_id):
    async with async_session() as session:
        return (await session.scalars(select(OrderItem).where(OrderItem.order_id == order_id))).all()
    

async def add_game(name, genre, daterelease, description, price):
    async with async_session() as session:
        session.add(Game(name=name, genre=genre, daterelease=daterelease, description=description, price=price))
        await session.commit()
        return