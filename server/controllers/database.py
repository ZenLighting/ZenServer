from server import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from server.model.sqlmodel import Base, Room, Household

engine = create_engine(settings.DATABASE_URI)
session_maker = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class SessionWrapper(object):
    def __init__(self):
        self.session: Session = session_maker()

    def __enter__(self):
        return self.session
    
    def __exit__(self, exc_type, exc_value, tb):
        self.session.close()