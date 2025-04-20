from BaseRepository import BaseREPO
from models import Device
from database import async_session
from sqlalchemy import select, insert, values, delete


class DeviceREPO(BaseREPO):
    model = Device
    
    @classmethod
    async def delete_by_mac_address(cls, mac_address, **kwargs):
        async with async_session() as session:
            query = delete(cls.model).where(cls.model.mac_address==mac_address)
            result = await session.execute(query)
            await session.commit()