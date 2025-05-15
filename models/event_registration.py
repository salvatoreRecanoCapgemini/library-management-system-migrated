

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

class EventRegistration(Base):
    __tablename__ = 'event_registration'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('library_event.id'))
    patron_id = Column(Integer, ForeignKey('patron.id'))
    registration_date = Column(DateTime, default=datetime.utcnow)
    attendance_status = Column(String(50), default='REGISTERED')

    event = relationship("LibraryEvent", backref="event_registrations")
    patron = relationship("Patron", backref="event_registrations")

    def __init__(self, event_id, patron_id, attendance_status='REGISTERED'):
        self.event_id = event_id
        self.patron_id = patron_id
        self.attendance_status = attendance_status

    def __repr__(self):
        return f"EventRegistration(id={self.id}, event_id={self.event_id}, patron_id={self.patron_id}, registration_date={self.registration_date}, attendance_status={self.attendance_status})"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()