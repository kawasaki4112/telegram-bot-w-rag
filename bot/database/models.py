import os, asyncio
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import String, Integer, DateTime, ForeignKey, event, Enum as SQLAEnum
from sqlalchemy.types import JSON
from datetime import datetime
from enum import Enum

db = os.getenv("DB", "sqlite+aiosqlite:///bot/database/db.sqlite3")
engine = create_async_engine(url=db)
async_session = async_sessionmaker(engine)

class BaseEntity(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    modified_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@event.listens_for(BaseEntity, "before_update", propagate=True)
def _update_modified_on(mapper, connection, target):
    target.modified_on = datetime.utcnow()

class UserRoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class User(BaseEntity):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRoleEnum] = mapped_column(SQLAEnum(UserRoleEnum), default=UserRoleEnum.user)

    requests: Mapped[list["Request"]] = relationship("Request", back_populates="user")

class Request(BaseEntity):
    __tablename__ = "requests"

    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    user_tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))

    user: Mapped["User"] = relationship("User", back_populates="requests")

class Embedding(BaseEntity):
    __tablename__ = "embeddings"

    url: Mapped[str] = mapped_column(String(2083), unique=True, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(JSON, nullable=False)
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(async_main())