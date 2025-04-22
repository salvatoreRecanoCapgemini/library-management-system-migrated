

from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    event_id = Column(Integer, ForeignKey('library_events.event_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    registration_date = Column(TIMESTAMP, default=func.current_timestamp())
    attendance_status = Column(VARCHAR, default='REGISTERED')