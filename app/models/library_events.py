

from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class LibraryEvents(db.Model):
    __tablename__ = 'library_events'
    __table_args__ = (UniqueConstraint('event_name', name='_unique_event_name'),)

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    participants = db.Column(db.Integer, nullable=False, default=0)
    event_status = db.Column(db.String(20), nullable=False, default='upcoming')

    def __init__(self, event_name, event_date, capacity):
        self.event_name = event_name
        self.event_date = event_date
        self.capacity = capacity

    def add_participant(self):
        if self.participants < self.capacity:
            self.participants += 1
        else:
            raise ValueError("Event is fully booked")

    def remove_participant(self):
        if self.participants > 0:
            self.participants -= 1
        else:
            raise ValueError("No participants to remove")

    def update_event_status(self, status):
        if status in ['upcoming', 'in progress', 'completed']:
            self.event_status = status
        else:
            raise ValueError("Invalid event status")