from sqlalchemy import BigInteger, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime, timedelta

from bot.data.config import DB_PATH

engine = create_async_engine(url=f'sqlite+aiosqlite:///{DB_PATH}')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    increment: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(30), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    query_history: Mapped['QueryHistory'] = relationship('QueryHistory', back_populates='user')
    appeals_history: Mapped['Appeals'] = relationship('Appeals', back_populates='user')

class QueryHistory(Base):
    __tablename__ = 'query_history'

    increment: Mapped[int] = mapped_column(primary_key=True)
    user_increment: Mapped[int] = mapped_column(ForeignKey('users.increment'))
    query: Mapped[str] = mapped_column(String(), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Settings(Base):
    __tablename__ = 'settings'
    
    increment: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    text: Mapped[str] = mapped_column(String(), nullable=False)
    value: Mapped[str] = mapped_column(String(), nullable=True)
    bool_value: Mapped[str] = mapped_column(Boolean(), nullable=True)

class Appeals(Base):
    __tablename__ = 'appeals'
    
    increment: Mapped[int] = mapped_column(primary_key=True)
    user_increment: Mapped[int] = mapped_column(ForeignKey('users.increment'))
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_replied: Mapped[bool] = mapped_column(Boolean, default=False)
    text: Mapped[str] = mapped_column(String(), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    

class Embedding(Base):
    __tablename__ = 'embeddings'
    
    increment: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[int] = mapped_column(unique=True, nullable=False)
    text: Mapped[int] = mapped_column(nullable=False)
    embedding: Mapped[int] = mapped_column(nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


