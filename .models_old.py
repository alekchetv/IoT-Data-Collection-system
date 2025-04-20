from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import MetaData
from pydantic import BaseModel
from sqlalchemy import ForeignKey, JSON, text
import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func


Base = declarative_base()
Base.metadata = MetaData()

class sensor_list(BaseModel):
    sensors: dict

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    block_state: Mapped[bool] = mapped_column(nullable=False)
    # device: Mapped[list["Device"]] = relationship(  # Связь 1 - M | /User/ - Device 
    #     "Device",
    #     back_populates="user",
    #     cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    # )

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    mac_address: Mapped[str]= mapped_column(nullable=False)
    block_state: Mapped[bool] = mapped_column(nullable=False)
    # id_user:Mapped[int] = mapped_column(ForeignKey('users.id'))
    # user: Mapped["User"] = relationship(        # Связь 1 - M | User - /Device/ 
    #     "User",
    #     back_populates="device"
    # )

    sensor: Mapped[list["Sensor"]] = relationship(  # Связь 1 - M | /Device/ - Sensor
        "Sensor",
        back_populates="device",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )

class Sensor(Base):
    __tablename__ = "sensors"
    
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    error_value: Mapped[float] = mapped_column(nullable=False)
    measurement_unit: Mapped[str] = mapped_column(nullable=False)
    id_device: Mapped[int] = mapped_column(ForeignKey('devices.id'))
    device: Mapped["Device"] = relationship(    # Связь 1 - M | Device - /Sensor/
        "Device",
        back_populates="sensor"
    )
    record: Mapped[list["Record"]] = relationship(  # Связь 1 - M | /Sensor/ - Record
        "Record",
        back_populates="sensor",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    value: Mapped[float] = mapped_column(nullable=False)
    id_sensor: Mapped[int] = mapped_column(ForeignKey('sensors.id'))
    sensor: Mapped["Sensor"] = relationship(    # Связь 1 - M | Sensor - /Record/
        "Sensor",
        back_populates="record"
    )
