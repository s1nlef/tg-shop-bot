from app.database.models import async_session
from app.database.models import User, Sneaker, SneakerSize, CartItem, Order, OrderItem
from sqlalchemy import select, delete, func


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(
                User(
                    tg_id=tg_id,
                )
            )
            await session.commit()


async def check_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_all_sneakers(page: int, per_page: int = 5):
    async with async_session() as session:
        return (
            await session.scalars(
                select(Sneaker).limit(per_page).offset(page * per_page)
            )
        ).all()


async def get_sneaker(sneaker_id: int):
    async with async_session() as session:
        return await session.scalar(select(Sneaker).where(Sneaker.id == sneaker_id))


async def get_sneakers_count() -> int:
    async with async_session() as session:
        return await session.scalar(select(func.count(Sneaker.id)))


async def get_sneakers_by_ids(sneaker_ids: list[int]):
    async with async_session() as session:
        return (
            await session.scalars(select(Sneaker).where(Sneaker.id.in_(sneaker_ids)))
        ).all()


async def add_to_cart(tg_id, sneaker_id):
    async with async_session() as session:
        cart = await session.scalar(
            select(CartItem).where(
                CartItem.tg_id == tg_id, CartItem.sneaker_id == sneaker_id
            )
        )
        if cart:
            cart.quantity += 1
        else:
            session.add(CartItem(tg_id=tg_id, sneaker_id=sneaker_id))
        await session.commit()


async def get_cart(tg_id):
    async with async_session() as session:
        return (
            await session.scalars(select(CartItem).where(CartItem.tg_id == tg_id))
        ).all()


async def remove_from_cart(tg_id, sneaker_id):
    async with async_session() as session:
        await session.execute(
            delete(CartItem).where(
                CartItem.tg_id == tg_id, CartItem.sneaker_id == sneaker_id
            )
        )
        await session.commit()


async def clean_cart(tg_id):
    async with async_session() as session:
        await session.execute(delete(CartItem).where(CartItem.tg_id == tg_id))
        await session.commit()


async def admin_change_balance(tg_id, balance):
    async with async_session() as session:
        admin = await session.scalar(select(User).where(User.tg_id == tg_id))
        if admin:
            admin.balance = balance
            await session.commit()


async def change_balance(tg_id, total_sum):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.balance -= total_sum
            await session.commit()


async def create_order(tg_id, order_table):
    async with async_session() as session:
        order = Order(tg_id=tg_id, price=order_table["total"])
        session.add(order)
        await session.flush()
        for sneaker, qty in zip(order_table["sneaker"], order_table["quantity"]):
            session.add(
                OrderItem(
                    order_id=order.id,
                    sneaker_id=sneaker.id,
                    quantity=qty,
                    price=sneaker.price * qty,
                )
            )
        await session.commit()
        return order.id


async def all_user_orders(tg_id):
    async with async_session() as session:
        return (
            await session.scalars(
                select(Order)
                .where(Order.tg_id == tg_id)
                .order_by(Order.created_at.desc())
            )
        ).all()


async def get_order_items(order_id):
    async with async_session() as session:
        return (
            await session.scalars(
                select(OrderItem).where(OrderItem.order_id == order_id)
            )
        ).all()


async def add_sneaker(brand, model, colorway, price, image_url):
    async with async_session() as session:
        session.add(
            Sneaker(
                brand=brand,
                model=model,
                colorway=colorway,
                price=int(price),
                image_url=image_url,
            )
        )
        await session.commit()
