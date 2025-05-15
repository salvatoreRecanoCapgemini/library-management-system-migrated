

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, DatabaseError
from datetime import datetime
from models import EventRegistration, LibraryEvent

class EventRegistrationRepository:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def register_for_event(self, event_id, patron_id):
        try:
            session = self.Session()
            existing_registration = session.query(EventRegistration).filter_by(event_id=event_id, patron_id=patron_id).first()
            if existing_registration:
                raise Exception('Patron is already registered for the event')
            event = session.query(LibraryEvent).filter_by(event_id=event_id).first()
            if not event:
                raise Exception('Event not found')
            if event.current_participants >= event.max_participants:
                raise Exception('Event is full')
            new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
            session.add(new_registration)
            session.commit()
            event = session.query(LibraryEvent).filter_by(event_id=event_id).first()
            if event:
                event.current_participants += 1
                session.commit()
        except IntegrityError as e:
            session.rollback()
            raise Exception('Database integrity error: ' + str(e))
        except DatabaseError as e:
            session.rollback()
            raise Exception('Database error: ' + str(e))
        finally:
            session.close()