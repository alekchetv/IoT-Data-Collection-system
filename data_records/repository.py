from BaseRepository import BaseREPO
from models import DataRecord
from database import async_session
from sqlalchemy import select, insert, values, delete

class DataRecordREPO(BaseREPO):
    model = DataRecord


    @classmethod
    async def get_last_rows(cls,rows, **kwargs):
        async with async_session() as session:
            query = select(cls.model).filter_by(**kwargs).order_by(DataRecord.created_date.desc()).limit(rows)
            models = await session.execute(query)
            return models.scalars().all()