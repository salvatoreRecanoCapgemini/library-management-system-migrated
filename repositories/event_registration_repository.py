

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///event_registration.db')
Base = declarative_base()

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
    attendance_status = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_event_registration(event_id, patron_id):
    try:
        event_registration = session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).first()
        if event_registration:
            return event_registration
        else:
            return None
    except Exception as e:
        session.rollback()
        raise e

def get_event_capacity(event_id):
    try:
        event = session.query(Event).filter_by(id=event_id).first()
        if event:
            return event.capacity
        else:
            return None
    except Exception as e:
        session.rollback()
        raise e

def check_event_capacity(event_id):
    try:
        event = session.query(Event).filter_by(id=event_id).first()
        if event:
            registrations = session.query(EventRegistration).filter_by(event_id=event_id).all()
            return len(registrations) < event.capacity
        else:
            return False
    except Exception as e:
        session.rollback()
        raise e

def create_event_registration(event_id, patron_id):
    try:
        if check_event_capacity(event_id):
            event_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
            session.add(event_registration)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        raise e