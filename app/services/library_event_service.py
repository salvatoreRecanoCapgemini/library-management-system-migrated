

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class EventStatus(PyEnum):
    SCHEDULED = 'SCHEDULED'
    CANCELLED = 'CANCELLED'

class AttendanceStatus(PyEnum):
    PENDING = 'PENDING'
    ATTENDED = 'ATTENDED'
    NO_SHOW = 'NO_SHOW'

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    status = Column(Enum(EventStatus))

class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    patron_id = Column(Integer)
    attendance_status = Column(Enum(AttendanceStatus))

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer)
    message = Column(String)

class LibraryEventService:
    def __init__(self, db_session):
        self.db_session = db_session

    def cancel_event(self, event_id):
        event = self.db_session.query(LibraryEvent).filter_by(id=event_id).first()
        if not event:
            raise ValueError("Event not found")

        if event.status == EventStatus.CANCELLED:
            raise ValueError("Event is already cancelled")

        event.status = EventStatus.CANCELLED
        self.db_session.commit()

        registrations = self.db_session.query(Registration).filter_by(event_id=event_id).all()
        for registration in registrations:
            registration.attendance_status = AttendanceStatus.NO_SHOW
            self.db_session.commit()

            notification = Notification(registration_id=registration.id, message="Event has been cancelled")
            self.db_session.add(notification)
            self.db_session.commit()

    def reschedule_event(self, event_id, new_date):
        event = self.db_session.query(LibraryEvent).filter_by(id=event_id).first()
        if not event:
            raise ValueError("Event not found")

        if event.status == EventStatus.CANCELLED:
            raise ValueError("Event is cancelled")

        if new_date < datetime.now():
            raise ValueError("New date is in the past")

        existing_events = self.db_session.query(LibraryEvent).filter_by(date=new_date).all()
        if existing_events:
            raise ValueError("New date conflicts with existing events")

        event.date = new_date
        self.db_session.commit()

        registrations = self.db_session.query(Registration).filter_by(event_id=event_id).all()
        for registration in registrations:
            notification = Notification(registration_id=registration.id, message="Event has been rescheduled to {}".format(new_date))
            self.db_session.add(notification)
            self.db_session.commit()