

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app

db = SQLAlchemy(app)

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    registration_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.id'))
    registration_date = db.Column(db.DateTime, default=datetime.now)
    attendance_status = db.Column(db.String(50), default='REGISTERED')
    __table_args__ = (db.UniqueConstraint('event_id', 'patron_id'),)

    def __init__(self, event_id, patron_id, registration_date=None, attendance_status='REGISTERED'):
        self.event_id = event_id
        self.patron_id = patron_id
        if registration_date is None:
            self.registration_date = datetime.now()
        else:
            self.registration_date = registration_date
        self.attendance_status = attendance_status

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e