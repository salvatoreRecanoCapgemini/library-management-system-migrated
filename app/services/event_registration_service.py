

from app.models.event_registration import EventRegistration
from app.models.library_event import LibraryEvent
from app import db
import logging

class EventRegistrationService:
    def register_patron_for_event(self, event_id, patron_id):
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise Exception('Invalid input parameters')
        if EventRegistration.query.filter_by(event_id=event_id, patron_id=patron_id).first():
            raise Exception('Patron already registered for this event')
        library_event = LibraryEvent.query.get(event_id)
        if library_event is None:
            raise Exception('Event not found')
        max_participants = library_event.max_participants
        current_participants = library_event.current_participants
        if current_participants >= max_participants:
            raise Exception('Event is full')
        event_registration = EventRegistration(event_id=event_id, patron_id=patron_id)
        db.session.add(event_registration)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error("Error registering patron: " + str(e))
            raise Exception("Error registering patron: " + str(e))