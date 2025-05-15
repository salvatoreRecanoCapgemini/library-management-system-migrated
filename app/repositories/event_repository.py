

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models import EventRegistration, LibraryEvent

class EventRepository:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def manage_event_registration(self, p_event_id, p_patron_id):
        if not isinstance(p_event_id, int) or not isinstance(p_patron_id, int):
            raise Exception("Invalid input parameters")

        existing_registration = self.session.query(EventRegistration).filter_by(event_id=p_event_id, patron_id=p_patron_id).first()
        if existing_registration:
            raise Exception("Patron is already registered for the event")

        event = self.session.query(LibraryEvent).filter_by(event_id=p_event_id).first()
        if not event:
            raise Exception("Event not found")

        max_participants = event.max_participants
        current_participants = event.current_participants
        if current_participants >= max_participants:
            raise Exception("Event is full")

        new_registration = EventRegistration(event_id=p_event_id, patron_id=p_patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
        self.session.add(new_registration)
        event.current_participants += 1
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise
        except Exception as e:
            self.session.rollback()
            raise Exception("Failed to register patron for the event") from e