

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class LibraryEvent(Base):
    __tablename__ = 'library_events'

    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(Date)
    max_participants = Column(Integer)
    participant_count = Column(Integer)

    patrons = relationship('Patron', secondary='event_registrations', backref='events')