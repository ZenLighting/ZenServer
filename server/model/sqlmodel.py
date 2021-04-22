from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()

class Household(Base, SerializerMixin):
    __tablename__ = "households"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Room(Base, SerializerMixin):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    household = Column(Integer, ForeignKey("households.id"))
    description = Column(String(256))

class Light(Base, SerializerMixin):
    __tablename__ = "lights"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(50))
    address = Column(String(50))
    port = Column(Integer)
    room = Column(Integer, ForeignKey("rooms.id"))
    length = Column(Integer)
    light_space = Column(String(1024))