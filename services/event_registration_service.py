

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum as PyEnum

engine = create_engine('sqlite:///event_registration.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class AttendanceStatus(PyEnum):
    REGISTERED = 'REGISTERED'
    ATTENDED = 'ATTENDED'

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    patron_id = Column(Integer)
    registration_date = Column(DateTime)
    attendance_status = Column(Enum(AttendanceStatus))

Base.metadata.create_all(engine)

def manage_event_registration(event_id, patron_id):
    if not isinstance(event_id, int) or not isinstance(patron_id, int):
        raise ValueError("Event ID and Patron ID must be integers")
    session = Session()
    try:
        existing_registration = session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).first()
        if existing_registration:
            return False
        event = session.query(Event).get(event_id)
        if event is None:
            raise ValueError("Event not found")
        if event.capacity <= 0:
            return False
        register_for_event(event_id, patron_id, session)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def register_for_event(event_id, patron_id, session):
    new_registration = EventRegistration(
        event_id=event_id,
        patron_id=patron_id,
        registration_date=datetime.now(),
        attendance_status=AttendanceStatus.REGISTERED
    )
    session.add(new_registration)

def get_event_capacity(event_id):
    session = Session()
    try:
        event = session.query(Event).get(event_id)
        if event is None:
            raise ValueError("Event not found")
        return event.capacity
    finally:
        session.close()