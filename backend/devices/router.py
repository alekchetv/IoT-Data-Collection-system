from fastapi import APIRouter, Request, HTTPException
from devices.schemas import Device
from devices.repository import DeviceREPO
from sensors.repository import SensorREPO, SensorTypeREPO
from devices.schemas import DeviceDelete
from ino_generator import json_pin_generate

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post("/add")
async def add_device(request: Request, device: Device):
    db_device = await DeviceREPO.find_one_or_none(mac_address=device.mac_address)
    if db_device:
        raise HTTPException(status_code=403, detail="Device already exist")
    await DeviceREPO.add(title=device.title, mac_address=device.mac_address, is_active=1)
    id_device = (await DeviceREPO.find_one_or_none(mac_address=device.mac_address)).id
    for sensor in device.sensors:
        await SensorREPO.add(name=sensor.name, error_value=sensor.error_value,
                             measurement_unit=sensor.measurement_unit, id_device=id_device,
                             id_sensor_type=sensor.sensor_type)
    await json_pin_generate(device)
    return HTTPException(status_code=200, detail="Device added succesfully")


@router.get("/get")
async def get_devices(request: Request):
    devices = await DeviceREPO.find_all()
    return devices


@router.delete("/delete")
async def delete_device(request: Request, device: DeviceDelete):
    await DeviceREPO.delete_by_mac_address(device.mac_address)
    return HTTPException(status_code=200, detail="Device deleted succesfully")
