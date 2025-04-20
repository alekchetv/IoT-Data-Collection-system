from __future__ import annotations
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


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    mac_address: Mapped[str]= mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)

    sensor: Mapped[list["Sensor"]] = relationship(  # Связь 1 - M | /Device/ - Sensor
        "Sensor",
        back_populates="device",
        cascade="all, delete-orphan"
    )


class Sensor(Base):
    __tablename__ = "sensor_list"
    
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    id_sensor_type: Mapped[int] = mapped_column(ForeignKey('sensor_types.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    error_value: Mapped[float] = mapped_column(nullable=False)
    measurement_unit: Mapped[str] = mapped_column(nullable=False)
    id_device: Mapped[int] = mapped_column(ForeignKey('devices.id', ondelete='CASCADE'))
    device: Mapped["Device"] = relationship(    # Связь 1 - M | Device - /Sensor/
        "Device",
        back_populates="sensor"
    )
    sensor_type: Mapped["SensorType"] = relationship(    # Связь 1 - M | SensorType - /Sensor/
        "SensorType",
        back_populates="sensor"
    )    
    data_record: Mapped[list["DataRecord"]] = relationship(  # Связь 1 - M | /Sensor/ - DataRecord
        "DataRecord",
        back_populates="sensor",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )


class SensorType(Base):
    __tablename__ = "sensor_types"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    sensor_name: Mapped[str] = mapped_column(nullable=False)
    sensor: Mapped[list["Sensor"]] = relationship(  # Связь 1 - M | /Device/ - Sensor
        "Sensor",
        back_populates="sensor_type",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )


class DataRecord(Base):
    __tablename__ = "data_records"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    value: Mapped[float] = mapped_column(nullable=False)
    id_sensor: Mapped[int] = mapped_column(ForeignKey('sensor_list.id', ondelete='CASCADE'))
    sensor: Mapped["Sensor"] = relationship(    # Связь 1 - M | Sensor - /Record/
        "Sensor",
        back_populates="data_record"
    )
