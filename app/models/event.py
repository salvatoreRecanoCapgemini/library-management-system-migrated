

from datetime import datetime
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///events.db')
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(Date)
    event_time = Column(Time)
    max_participants = Column(Integer)
    registered_participants = Column(Integer)
    status = Column(String)

    def __init__(self, event_id: int, event_name: str, event_date: datetime, event_time: datetime, max_participants: int, registered_participants: int, status: str):
        self.event_id = event_id
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.max_participants = max_participants
        self.registered_participants = registered_participants
        self.status = status

    @staticmethod
    def get_events(date_range: List[datetime]) -> List['Event']:
        if not isinstance(date_range, list) or len(date_range) != 2:
            raise ValueError("Invalid date range")
        if not all(isinstance(date, datetime) for date in date_range):
            raise ValueError("Invalid date range")
        if date_range[0] > date_range[1]:
            raise ValueError("Invalid date range")

        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            events = session.query(Event).filter(Event.event_date >= date_range[0].date(), Event.event_date <= date_range[1].date()).all()
            return events
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

Base.metadata.create_all(engine)