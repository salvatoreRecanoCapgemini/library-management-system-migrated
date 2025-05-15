

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import EventRegistration, LibraryEvent

class EventRegistrationController:
    def __init__(self, event_registration_service):
        if event_registration_service is None:
            raise Exception("Event registration service cannot be None")
        self.event_registration_service = event_registration_service

    def register_patron_for_event(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception("Event ID and Patron ID must be integers")
        try:
            session = self.event_registration_service.create_session()
            existing_registration = session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).first()
            if existing_registration:
                raise Exception("Patron is already registered for the event")
            event = session.query(LibraryEvent).filter_by(event_id=event_id).first()
            if event is None:
                raise Exception("Event does not exist")
            max_participants = event.max_participants
            current_participants = event.current_participants
            if current_participants >= max_participants:
                raise Exception("Event is full")
            new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
            session.add(new_registration)
            session.commit()
            event.current_participants += 1
            session.commit()
            return 'Patron registered for event successfully'
        except Exception as e:
            session.rollback()
            raise e