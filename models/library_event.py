

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LibraryEvent(db.Model):
    __tablename__ = 'library_events'
    event_id = db.Column(db.Integer, primary_key=True)
    current_participants = db.Column(db.Integer, default=0)

    def __init__(self, event_id, current_participants):
        self.event_id = event_id
        self.current_participants = current_participants

    def __repr__(self):
        return f"LibraryEvent('{self.event_id}', '{self.current_participants}')"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}