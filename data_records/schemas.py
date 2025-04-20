from pydantic import BaseModel
from typing import List
from sensors.schemas import SensorDataForm

class DataRecordForm(BaseModel):
    mac_address: str
    sensors: List[SensorDataForm]

class GetDataRecordForm(BaseModel):
    mac_address: str

class PostDataRecordForm(BaseModel):
    mac_address: str
    sensor_type: str
    output_data: float

