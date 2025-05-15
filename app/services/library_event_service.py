

import json
from datetime import datetime
from typing import List, Dict

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    date = Column(DateTime)

class Registrant(Base):
    __tablename__ = 'registrants'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    attendance_status = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    action = Column(String)
    event_id = Column(Integer)
    event_data = Column(JSON)

Base.metadata.create_all(engine)

class LibraryEventService:
    def __init__(self):
        self.session = Session()

    def cancel_event(self, event_id: int):
        event = self.session.query(Event).get(event_id)
        if event:
            event.status = 'CANCELLED'
            registrants = self.session.query(Registrant).filter_by(event_id=event_id).all()
            for registrant in registrants:
                registrant.attendance_status = 'NO_SHOW'
            self.session.commit()
            self.process_notifications(registrants)
            self.log_notifications_and_conflicts('CANCEL', event_id, {'status': event.status})

    def reschedule_event(self, event_id: int, event_data: Dict):
        if self.validate_new_date(event_data):
            event = self.session.query(Event).get(event_id)
            if event:
                event.date = event_data['new_date']
                self.session.commit()
                registrants = self.session.query(Registrant).filter_by(event_id=event_id).all()
                self.process_notifications(registrants)
                self.log_notifications_and_conflicts('reschedule', event_id, event_data)

    def update_event_status(self, event_id: int, status: str):
        event = self.session.query(Event).get(event_id)
        if event:
            event.status = status
            self.session.commit()

    def update_attendance_status(self, registrants: List[Registrant], status: str):
        for registrant in registrants:
            registrant.attendance_status = status
        self.session.commit()

    def process_notifications(self, registrants: List[Registrant]):
        for registrant in registrants:
            # Process notification for registrant
            print(f"Notification sent to registrant {registrant.id}")

    def log_notifications_and_conflicts(self, action: str, event_id: int, event_data: Dict):
        log = AuditLog(action=action, event_id=event_id, event_data=event_data)
        self.session.add(log)
        self.session.commit()

    def validate_new_date(self, event_data: Dict) -> bool:
        new_date = datetime.strptime(event_data['new_date'], '%Y-%m-%d %H:%M:%S')
        existing_events = self.session.query(Event).filter(Event.date == new_date).all()
        if existing_events:
            return False
        return new_date > datetime.now()