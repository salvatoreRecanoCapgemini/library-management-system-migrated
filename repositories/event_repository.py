

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('library_events.id'))
    patron_id = Column(Integer)
    registration_date = Column(DateTime, default=datetime.now)
    attendance_status = Column(String(50))
    event = relationship("LibraryEvent", backref="registrations")

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    id = Column(Integer, primary_key=True)
    current_participants = Column(Integer, default=0)
    event_status = Column(String(50), default='SCHEDULED')
    event_date = Column(DateTime)

Base.metadata.create_all(engine)

def manage_library_events(action, event_id, event_data):
    if action == 'cancel':
        affected_registrants = session.query(EventRegistration).filter_by(event_id=event_id).all()
        for registrant in affected_registrants:
            registrant.attendance_status = 'NO_SHOW'
        session.commit()
        library_event = session.query(LibraryEvent).filter_by(id=event_id).first()
        library_event.event_status = 'CANCELLED'
        session.commit()
        process_notifications(affected_registrants)
    elif action == 'reschedule':
        new_date = event_data['new_date']
        validate_new_date(new_date)
        schedule_conflicts = session.query(EventRegistration).filter_by(event_id=event_id).all()
        for conflict in schedule_conflicts:
            conflict.attendance_status = 'SCHEDULE_CONFLICT'
        session.commit()
        library_event = session.query(LibraryEvent).filter_by(id=event_id).first()
        library_event.event_date = new_date
        library_event.event_status = 'RESCHEDULED'
        session.commit()
        notify_patrons(schedule_conflicts)

def register_for_event(event_id, patron_id):
    new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, attendance_status='REGISTERED')
    session.add(new_registration)
    session.commit()
    library_event = session.query(LibraryEvent).filter_by(id=event_id).first()
    library_event.current_participants += 1
    session.add(library_event)
    session.commit()

def process_notifications(registrants):
    for registrant in registrants:
        logging.info(f"Sending notification to patron {registrant.patron_id}")

def validate_new_date(new_date):
    if new_date < datetime.now():
        raise ValueError("New date cannot be in the past")

def notify_patrons(conflicts):
    for conflict in conflicts:
        logging.info(f"Sending notification to patron {conflict.patron_id} about schedule conflict")