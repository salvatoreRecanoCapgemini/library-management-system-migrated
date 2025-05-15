

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_date = Column(DateTime)
    event_time = Column(DateTime)
    max_participants = Column(Integer)
    registered_participants = Column(Integer)
    status = Column(String)

class EventRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.ERROR)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

    def get_events(self, date_range):
        if not isinstance(date_range, list) or len(date_range) != 2:
            self.log.error("Invalid date range")
            return []
        start_date, end_date = date_range
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            self.log.error("Invalid date format")
            return []
        try:
            events = self.session.query(Event).filter(Event.event_date.between(start_date, end_date)).all()
            return events
        except Exception as e:
            self.log.error(e)
            return []

    def get_events_raw_query(self, start_date, end_date):
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            self.log.error("Invalid date format")
            return []
        try:
            query = "SELECT * FROM events WHERE event_date >= :start_date AND event_date <= :end_date"
            params = {"start_date": start_date, "end_date": end_date}
            events = self.session.execute(query, params)
            return events
        except Exception as e:
            self.log.error(e)
            return []