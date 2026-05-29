from sqlalchemy import BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL don't set in environment")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")


class Sneaker(Base):
    __tablename__ = "sneakers"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(64))
    model: Mapped[str] = mapped_column(String(128))
    colorway: Mapped[str] = mapped_column(String(64))
    price: Mapped[int] = mapped_column()
    image_url: Mapped[str] = mapped_column(String(256))


class SneakerSize(Base):
    __tablename__ = "sneakers_size"
    id: Mapped[int] = mapped_column(primary_key=True)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    size: Mapped[str] = mapped_column(String(8))
    stock: Mapped[int] = mapped_column(default=0)


class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    size: Mapped[str] = mapped_column(String(8))
    user: Mapped["User"] = relationship(back_populates="cart_items")
    sneaker: Mapped["Sneaker"] = relationship()


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    price: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(20), default="completed")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "orders_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    sneaker_id: Mapped[int] = mapped_column(ForeignKey("sneakers.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[int] = mapped_column()
    order: Mapped["Order"] = relationship(back_populates=("items"))
    sneaker: Mapped["Sneaker"] = relationship()
