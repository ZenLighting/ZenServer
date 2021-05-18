import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

print(settings.DB_URI)
engine = create_engine(settings.DB_URI)
session_maker = sessionmaker(bind=engine)

class DatabaseSession(object):

    def __init__(self):
        self.session: Session = session_maker()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_value, tb):
        self.session.close()