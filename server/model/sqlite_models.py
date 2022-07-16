from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import pydantic
from typing import List, Any, Optional

Base = declarative_base()


"""room_light_association = Table(
    "light_room_association",
    Base.metadata,
    Column("room_name", ForeignKey("room.name")),
    Column("light_id", ForeignKey("lightdevice.id"))
)"""

class LightDeviceORM(Base):
    __tablename__ = "lightdevice"

    id=Column(Integer, primary_key=True)
    name = Column(String)
    grid_string = Column(String) # grid string is a representation of a light matrix where noled is rep by - and led is rep by x
    # number of LEDS can be determined by reading x's newlines represent rows
    last_address = Column(String) # the last address we have seen over network
    rooms = relationship("RoomLightAssociation", back_populates="light")

class PartialDevice(pydantic.BaseModel):
    name: str
    last_address: str


class LightDeviceModel(pydantic.BaseModel):
    id: Optional[int]
    name: str
    grid_string: str
    last_address: Optional[str]
    rooms: Any

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

    @classmethod
    def create_from_partial(cls, partial: PartialDevice, grid_string: str):
        return LightDeviceModel(name=partial.name, grid_string=grid_string, last_address=partial.last_address)

class RoomLightAssociation(Base):
    __tablename__="light_room_association"
    room_name = Column(String, ForeignKey("room.name"), primary_key=True)
    light_id = Column(String, ForeignKey("lightdevice.id"), primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    room = relationship("RoomOrm", back_populates="lights")
    light = relationship("LightDeviceORM", back_populates="rooms")

class RoomOrm(Base):
    __tablename__ = "room"

    name=Column(String, primary_key=True)
    lights=relationship("RoomLightAssociation", back_populates="room")

class RoomModel(pydantic.BaseModel):
    name: str
    lights: Any

    class Config:
        orm_mode=True


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
