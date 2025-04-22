

from datetime import datetime
from app import db
from app.models import EventRegistration, LibraryEvent
from flask import current_app

def register_for_event(event_id, patron_id):
    if not event_id or not patron_id:
        raise ValueError("Event ID and Patron ID are required")

    try:
        event_registration = EventRegistration(event_id=event_id, patron_id=patron_id)
        event_registration.registration_date = datetime.now(current_app.config['TIMEZONE'])
        event_registration.attendance_status = 'REGISTERED'
        db.session.add(event_registration)
        library_event = LibraryEvent.query.with_for_update().get(event_id)
        if library_event is None:
            raise ValueError("Event not found")
        library_event.current_participants += 1
        db.session.add(library_event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

register_for_event.__doc__ = """
Registers a patron for an event, updating event registrations and participant count.

Args:
    event_id (int): The ID of the event to register for.
    patron_id (int): The ID of the patron registering for the event.

Raises:
    ValueError: If event_id or patron_id is missing, or if the event is not found.
    Exception: If a database error occurs.
"""