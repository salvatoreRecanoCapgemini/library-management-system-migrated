

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.event_registration import EventRegistration
from models.library_event import LibraryEvent
from datetime import datetime
import logging

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

def manage_event_registration(event_id, patron_id):
    if not event_id or not patron_id:
        raise Exception('Event ID and Patron ID are required')

    session = Session()
    try:
        existing_registration = session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).first()
        if existing_registration:
            raise Exception('Patron is already registered for the event')

        event = session.query(LibraryEvent).filter_by(event_id=event_id).first()
        if event is None:
            raise Exception('Event not found')

        if event.current_participants >= event.max_participants:
            raise Exception('Event is full')

        new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
        session.add(new_registration)
        session.commit()

        event.current_participants += 1
        session.add(event)
        session.commit()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        session.rollback()
        raise
    finally:
        session.close()