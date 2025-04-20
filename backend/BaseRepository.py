from database import async_session
from sqlalchemy import select, insert, values, delete


class BaseREPO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            models = await session.execute(query)
            return models.scalars().one_or_none()

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session() as session:
            query = select(cls.model).filter_by(**kwargs)
            models = await session.execute(query)
            return models.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            models = await session.execute(query)
            return models.scalar_one_or_none()

    @classmethod
    async def add(cls, **kwargs):
        async with async_session() as session:
            query = insert(cls.model).values(**kwargs)
            result = await session.execute(query)
            await session.commit()


