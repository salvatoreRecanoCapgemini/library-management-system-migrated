

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('library_events.event_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    registration_date = Column(DateTime, default=datetime.now())
    attendance_status = Column(String)

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    event_id = Column(Integer, primary_key=True)
    current_participants = Column(Integer)
    max_participants = Column(Integer)

Session = sessionmaker(bind=engine)
session = Session()

class EventRegistrationRepository:
    def manage_event_registration(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception('Invalid input parameters')
        existing_registration = session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).first()
        if existing_registration:
            raise Exception('Patron already registered for this event')
        event = session.query(LibraryEvent).filter_by(event_id=event_id).first()
        if not event:
            raise Exception('Event not found')
        if event.current_participants >= event.max_participants:
            raise Exception('Event is full')
        new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, attendance_status='REGISTERED')
        session.add(new_registration)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception('Error occurred while registering patron')
        finally:
            session.close()

    def get_event_registration(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception('Invalid input parameters')
        return session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).first()

    def insert_event_registration(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception('Invalid input parameters')
        registration = EventRegistration(event_id=event_id, patron_id=patron_id)
        session.add(registration)
        session.commit()

    def create_event_registration(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception('Invalid input parameters')
        new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
        session.add(new_registration)
        session.commit()

    def update_event_registration(self, event_id, patron_id, attendance_status):
        if not isinstance(event_id, int) or not isinstance(patron_id, int) or not isinstance(attendance_status, str):
            raise Exception('Invalid input parameters')
        registration = self.get_event_registration(event_id, patron_id)
        if registration:
            registration.attendance_status = attendance_status
            session.commit()

    def delete_event_registration(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception('Invalid input parameters')
        registration = self.get_event_registration(event_id, patron_id)
        if registration:
            session.delete(registration)
            session.commit()

    def register_for_event(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception('Invalid input parameters')
        new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, attendance_status='REGISTERED')
        session.add(new_registration)
        session.commit()
        event = session.query(LibraryEvent).filter_by(event_id=event_id).first()
        if event:
            event.current_participants += 1
            session.commit()
        else:
            raise Exception('Event not found')