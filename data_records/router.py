from fastapi import APIRouter, Request
from data_records.schemas import PostDataRecordForm, GetDataRecordForm
from sensors.repository import SensorTypeREPO, SensorREPO
from data_records.repository import DataRecordREPO
from devices.repository import DeviceREPO

router = APIRouter(
    prefix="/data_records",
)


@router.post("/send_data")
async def send_data(request: Request, data: PostDataRecordForm):
    print(data)
    sensor_type_id = (await SensorTypeREPO.find_one_or_none(sensor_name=data.sensor_type)).id
    device_id = (await DeviceREPO.find_one_or_none(mac_address=data.mac_address)).id
    sensor_id = (await SensorREPO.find_one_or_none(id_device=device_id, id_sensor_type=sensor_type_id)).id
    await DataRecordREPO.add(value=data.output_data, id_sensor=sensor_id)


@router.post("/get_data")
async def get_data(request: Request, data:GetDataRecordForm):
    device = await DeviceREPO.find_one_or_none(mac_address=data.mac_address)
    device_id = device.id

    sensors = await SensorREPO.find_all(id_device=device_id)
    result = []
    for sensor in sensors:
        sensor_name = (await SensorTypeREPO.find_by_id(sensor.id_sensor_type)).sensor_name
        records = (await DataRecordREPO.get_last_rows(10, id_sensor=sensor.id))
        result.append({"sensor_type": sensor_name, "output_data": records})
    return {"device_title":device.title, "data": result}