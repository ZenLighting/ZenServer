from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import pydantic
from typing import List, Any, Optional

Base = declarative_base()

class LightDeviceORM(Base):
    __tablename__ = "lightdevice"

    id=Column(Integer, primary_key=True)
    name = Column(String)
    grid_string = Column(String) # grid string is a representation of a light matrix where noled is rep by - and led is rep by x
    # number of LEDS can be determined by reading x's newlines represent rows
    last_address = Column(String) # the last address we have seen over network

class PartialDevice(pydantic.BaseModel):
    name: str
    last_address: str


class LightDeviceModel(pydantic.BaseModel):
    id: Optional[int]
    name: str
    grid_string: str
    last_address: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

    @classmethod
    def create_from_partial(cls, partial: PartialDevice, grid_string: str):
        return LightDeviceModel(name=partial.name, grid_string=grid_string, last_address=partial.last_address)



"""class LightRoomORM(Base):
    __tablename__ = "room"

    name = Column(String, primary_key=True)

class LightRoomModel(pydantic.BaseModel):
    name: str

    class Config:
        orm_mode = True

class LightRoomDeviceORM(Base):
    __tablename__ = "light_room_device"

    room=Column(String, ForeignKey("room.name"), primary_key=True)
    device=Column(Integer, ForeignKey("lightdevice.id"), primary_key=True)

class LightRoomDeviceModel(pydantic.BaseModel):
    room: String
    device: Integer

    class Config:
        orm_mode = True"""
