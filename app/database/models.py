from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import date, datetime
engine = create_async_engine("sqlite+aiosqlite:///tg-shop.sqlite3")
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger,  unique=True)
    balance: Mapped[int] = mapped_column(default=0)
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")

class Game(Base):
    __tablename__= "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    genre: Mapped[str] = mapped_column(String(64))
    daterelease: Mapped[date] = mapped_column()
    description: Mapped[str] = mapped_column(String(1024))
    price: Mapped[int] = mapped_column()

class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))    
    quantity: Mapped[int] = mapped_column(default=1)
    user: Mapped["User"] = relationship(back_populates="cart_items")
    game: Mapped["Game"] = relationship()

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"))    
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))    
    price: Mapped[int] = mapped_column()    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)