from pydantic import BaseModel


class SensorType(BaseModel):
    sensor_name: str


class Sensor(BaseModel):
    name: str
    sensor_type: int
    error_value: float
    measurement_unit: str
    pin: int


class SensorDataForm(BaseModel):
    sensor_type: str
    output_data: float


class CodeSamples(BaseModel):
    glob: str
    setup: str
    loop: str


class SensorPinGenerator(BaseModel):
    sensor_name: CodeSamples
    