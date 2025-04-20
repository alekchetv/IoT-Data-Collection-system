from pydantic import BaseModel
from sensors.schemas import Sensor
from typing import List


class Device(BaseModel):
    title: str
    mac_address: str
    ip_address: str
    sensors: List[Sensor]


class DeviceDelete(BaseModel):
    mac_address: str

