

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(Date)
    capacity = Column(Integer)
    participants = Column(Integer)

    patrons = relationship('Patron', secondary='event_registrations', backref='events')