from BaseRepository import BaseREPO
from models import Sensor, SensorType


class SensorREPO(BaseREPO):
    model = Sensor


class SensorTypeREPO(BaseREPO):
    model = SensorType