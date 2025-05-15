

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models import LibraryEvent, EventRegistration

class EventRegistrationService:
    def __init__(self, db_session):
        self.db_session = db_session

    def check_event_capacity(self, event_id):
        try:
            event = self.db_session.query(LibraryEvent).filter_by(id=event_id).one()
            if event.current_participants >= event.max_participants:
                raise Exception('Event is full')
        except NoResultFound:
            raise Exception('Event not found')

    def is_patron_registered(self, event_id, patron_id):
        try:
            registration = self.db_session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).one()
            raise Exception('Patron is already registered')
        except NoResultFound:
            pass

    def register_patron_for_event(self, event_id, patron_id):
        self.check_event_capacity(event_id)
        self.is_patron_registered(event_id, patron_id)
        event_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
        self.db_session.add(event_registration)
        try:
            self.db_session.commit()
            self.update_event_participants_count(event_id)
        except IntegrityError:
            self.db_session.rollback()
            raise

    def update_event_participants_count(self, event_id):
        try:
            event = self.db_session.query(LibraryEvent).filter_by(id=event_id).one()
            event.current_participants += 1
            self.db_session.commit()
        except NoResultFound:
            raise Exception('Event not found')
        except Exception as e:
            self.db_session.rollback()
            raise