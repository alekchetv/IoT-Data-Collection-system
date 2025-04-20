from fastapi import FastAPI, Request
from models import sensor_list
import uvicorn
from sensors.repository import SensorTypeREPO
from users.router import router as router_users
from devices.router import router as router_devices
from sensors.router import router as router_sensors
from data_records.router import router as router_data_records
from fastapi.middleware.cors import CORSMiddleware
from ino_generator import script
import asyncio
from config import IP_HOST
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await script()
    yield

app = FastAPI(
    title="ESP32 API",
    lifespan=lifespan
)


origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_users)
app.include_router(router_devices)
app.include_router(router_sensors)
app.include_router(router_data_records)



@app.post("/upload")
async def upload(request: Request, sensor_list: sensor_list):
    for sensor in sensor_list.sensors:
        print(sensor)


if __name__=="__main__":
    uvicorn.run(app, host="192.168.39.9", port=8000)