from sensors.repository import SensorREPO, SensorTypeREPO
from fastapi import APIRouter, Request, HTTPException
from sensors.schemas import SensorType

router = APIRouter(
    prefix="/sensors",
    tags=["Датчики"]
)


@router.get("/get_types")
async def get_all_sensor_types():
    all_types = await SensorTypeREPO.find_all()
    return all_types


@router.post("/add_type")
async def add_sensor_types(request: Request, sensor_type: SensorType):
    current_type = await SensorTypeREPO.find_one_or_none(sensor_name=sensor_type.sensor_name)
    if not current_type:
        await SensorTypeREPO.add(sensor_name=sensor_type.sensor_name)
        return 1
    else:
        raise HTTPException(status_code=403, detail="Sensor type already exists")