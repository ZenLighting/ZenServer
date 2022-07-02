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

class LightDeviceModel(pydantic.BaseModel):
    id: Optional[int]
    name: str
    grid_string: str
    last_address: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True