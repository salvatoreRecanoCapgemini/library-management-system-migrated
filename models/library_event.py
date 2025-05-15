

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LibraryEvent(Base):
    __tablename__ = 'library_events'

    event_id = Column(Integer, primary_key=True)
    max_participants = Column(Integer)
    current_participants = Column(Integer)