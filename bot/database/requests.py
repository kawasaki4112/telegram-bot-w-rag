from bot.database.models import async_session
from bot.database.models import User, Request, Embedding
from sqlalchemy import select, update, delete

class CRUDUtility:
    def __init__(self, model):
        self.model = model

    async def create(self, **kwargs):
        async with async_session() as session:
            instance = self.model(**kwargs)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def get(self, **filters):
        async with async_session() as session:
            query = select(self.model).filter_by(**filters)
            result = await session.scalar(query)
            return result

    async def get_list(self, **filters):
        async with async_session() as session:
            query = select(self.model).filter_by(**filters)
            result = await session.scalars(query)
            return result.all()

    async def update(self, filters: dict, updates: dict):
        async with async_session() as session:
            query = update(self.model).filter_by(**filters).values(**updates).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await session.commit()

    async def delete(self, **filters):
        async with async_session() as session:
            query = delete(self.model).filter_by(**filters).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await session.commit()

user_crud = CRUDUtility(User)
request_crud = CRUDUtility(Request)
embedding_crud = CRUDUtility(Embedding)

