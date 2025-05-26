from database.models import async_session
from database.models import User, QueryHistory, Settings, Appeals, Embedding
from sqlalchemy import select, update, func
import utils.const_functions as ut


#####################################################################################
######################################## Set ########################################
#####################################################################################

async def set_user(user_id: int, username: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        if not user:
            session.add(User(user_id=user_id, username=username))
            await session.commit()
        elif user.username != username:
            user.username = username
            await session.commit()

async def set_appeal(user_id: int, text: str, message_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User.increment).where(User.user_id == user_id))
        session.add(Appeals(user_increment=user.increment, message_id=message_id, text=text))
        await session.commit()

async def get_appeals() -> list[Appeals]:
    async with async_session() as session:
        appeals = await session.scalars(select(Appeals))
        return appeals.all()

async def get_user(user_id: int = None, username: str = None) -> User:
    async with async_session() as session:
        if user_id:
            return await session.scalar(select(User).where(User.user_id == user_id))
        elif username:
            return await session.scalar(select(User).where(User.username == username))

async def get_admins() -> list[int]:
    async with async_session() as session:
        admins = await session.scalars(select(User.user_id).where(User.is_admin == True))
        return admins.all()
    
