

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.exc import IntegrityError, InvalidRequestError

Base = declarative_base()

class EventRegistration(Base):
    __tablename__ = 'event_registrations'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('library_events.event_id'), primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'), primary_key=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    attendance_status = Column(String)

    event = relationship('LibraryEvent', backref='event_registrations')
    patron = relationship('Patron', backref='event_registrations')

    def __init__(self, event_id, patron_id, registration_date=None, attendance_status=None):
        self.event_id = event_id
        self.patron_id = patron_id
        if registration_date is None:
            registration_date = datetime.now()
        self.registration_date = registration_date
        self.attendance_status = attendance_status

    def __repr__(self):
        return f"EventRegistration(id={self.id}, event_id={self.event_id}, patron_id={self.patron_id}, registration_date={self.registration_date}, attendance_status={self.attendance_status})"

engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_event_registration(event_id, patron_id, registration_date=None, attendance_status=None):
    try:
        event_registration = EventRegistration(event_id, patron_id, registration_date, attendance_status)
        session.add(event_registration)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Error adding event registration: {e}")
    except InvalidRequestError as e:
        session.rollback()
        print(f"Error adding event registration: {e}")

def get_event_registration(id):
    try:
        event_registration = session.query(EventRegistration).filter_by(id=id).first()
        return event_registration
    except Exception as e:
        print(f"Error getting event registration: {e}")

def update_event_registration(id, event_id=None, patron_id=None, registration_date=None, attendance_status=None):
    try:
        event_registration = session.query(EventRegistration).filter_by(id=id).first()
        if event_registration:
            if event_id:
                event_registration.event_id = event_id
            if patron_id:
                event_registration.patron_id = patron_id
            if registration_date:
                event_registration.registration_date = registration_date
            if attendance_status:
                event_registration.attendance_status = attendance_status
            session.commit()
        else:
            print("Event registration not found")
    except Exception as e:
        session.rollback()
        print(f"Error updating event registration: {e}")

def delete_event_registration(id):
    try:
        event_registration = session.query(EventRegistration).filter_by(id=id).first()
        if event_registration:
            session.delete(event_registration)
            session.commit()
        else:
            print("Event registration not found")
    except Exception as e:
        session.rollback()
        print(f"Error deleting event registration: {e}")