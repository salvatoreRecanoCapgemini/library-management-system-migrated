

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import EventRegistration, LibraryEvent

class EventRepository:
    def __init__(self, session):
        self.session = session

    def manage_event_registration(self, p_event_id, p_patron_id):
        """
        Manages event registration and updates event capacity information.

        Args:
            p_event_id (int): The ID of the event.
            p_patron_id (int): The ID of the patron.

        Raises:
            Exception: If the patron is already registered for the event or if the event is full.
        """
        existing_registration = self.session.query(EventRegistration).filter_by(event_id=p_event_id, patron_id=p_patron_id).first()
        if existing_registration is not None:
            raise Exception("Patron is already registered for the event")

        event = self.session.query(LibraryEvent).filter_by(event_id=p_event_id).first()
        if event is None:
            raise Exception("Event not found")

        max_participants = event.max_participants
        current_participants = event.current_participants

        if current_participants >= max_participants:
            raise Exception("Event is full")

        new_registration = EventRegistration(event_id=p_event_id, patron_id=p_patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
        self.session.add(new_registration)

        try:
            event.current_participants += 1
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise Exception("Failed to register patron for the event")