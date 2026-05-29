from typing import Sized
from app.database.models import async_session
from app.database.models import User, Sneaker, SneakerSize, CartItem, Order, OrderItem
from sqlalchemy import distinct, select, delete, func


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


async def get_sneakers_filtered(
    page: int = 0,
    per_page: int = 5,
    brand_name: str | None = None,
    size: str | None = None,
    price_max: int | None = None,
):
    async with async_session() as session:
        query = select(Sneaker)
        if brand_name:
            query = query.where(Sneaker.brand == brand_name)

        if price_max:
            query = query.where(Sneaker.price <= price_max)

        if size:
            query = (
                query.join(SneakerSize)
                .where(SneakerSize.size == size)
                .where(SneakerSize.stock > 0)
            )
        query = query.limit(per_page).offset(page * per_page)
        return (await session.scalars(query)).all()


async def get_distinct_brands(page: int | None, per_page: int | None = 5):
    async with async_session() as session:
        if page is not None and per_page is not None:
            return (
                await session.scalars(
                    select(Sneaker.brand)
                    .distinct()
                    .limit(per_page)
                    .offset(page * per_page)
                )
            ).all()
        else:
            return await session.scalar(select(func.count(Sneaker.brand.distinct())))


async def get_all_sneakers(page: int, per_page: int = 5, brand_name: str = ""):
    async with async_session() as session:
        return (
            await session.scalars(
                select(Sneaker)
                .where(Sneaker.brand == brand_name)
                .limit(per_page)
                .offset(page * per_page)
            )
        ).all()


async def get_sneaker(sneaker_model: str | None = None, sneaker_id: int | None = None):
    async with async_session() as session:
        if sneaker_id is not None:
            return await session.scalar(
                select(Sneaker).where(Sneaker.id == sneaker_id)
            )
        else:
            return await session.scalar(
                select(Sneaker).where(Sneaker.model == sneaker_model)
            )


async def get_sneaker_size(sneaker_id: int):
    async with async_session() as session:
        if sneaker_id:
            return (
                await session.scalars(
                    select(SneakerSize).where(SneakerSize.sneaker_id == sneaker_id)
                )
            ).all()


async def get_sneakers_brand_count(brand: str) -> int:
    async with async_session() as session:
        return await session.scalar(
            select(func.count(distinct(Sneaker.model))).where(Sneaker.brand == brand)
        )


async def get_sneakers_by_ids(sneaker_ids: list[int]):
    async with async_session() as session:
        return (
            await session.scalars(select(Sneaker).where(Sneaker.id.in_(sneaker_ids)))
        ).all()


async def add_to_cart(tg_id, sneaker_id, size):
    async with async_session() as session:
        cart = await session.scalar(
            select(CartItem).where(
                CartItem.tg_id == tg_id, CartItem.sneaker_id == sneaker_id
            )
        )
        if cart:
            cart.quantity += 1
        else:
            session.add(CartItem(tg_id=tg_id, sneaker_id=sneaker_id, size=size))
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


async def create_order(tg_id, order_table):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return None

        order = Order(tg_id=tg_id, price=order_table["total"])
        session.add(order)
        await session.flush()
        items = order_table["items"]
        for sneaker in items:
            session.add(
                OrderItem(
                    order_id=order.id,
                    sneaker_id=sneaker["sneaker_id"],
                    quantity=sneaker["quantity"],
                    price=sneaker["price"] * sneaker["quantity"],
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


async def add_sneaker(brand, model, colorway, price, image_url, size_table):
    async with async_session() as session:
        sneaker = Sneaker(
            brand=brand,
            model=model,
            colorway=colorway,
            price=int(price),
            image_url=image_url,
        )
        session.add(sneaker)
        await session.flush()
        for size, stock in size_table.items():
            session.add(SneakerSize(sneaker_id=sneaker.id, size=size, stock=int(stock)))
        await session.commit()
