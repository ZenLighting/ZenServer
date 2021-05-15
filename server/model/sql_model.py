from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from server.model.database import engine

Base = declarative_base()


class LightDevice(Base):
    __tablename__ = "light"

    device_id = Column(String, primary_key=True)
    light_amount = Column(Integer)
    description = Column(String)
    light_mapping = Column(String)
    room = Column(String, nullable=True)
    room_x = Column(Integer, nullable=True)
    room_y = Column(Integer, nullable=True)

class Room(Base):
    __tablename__ = "room"

    id=Column(Integer, primary_key=True)
    room_name = Column(String)

print("CREATED")
Base.metadata.create_all(engine)