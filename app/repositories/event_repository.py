

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('library_event.id'))
    library_event = db.relationship('LibraryEvent', backref=db.backref('event_registrations', lazy=True))

    def __init__(self, event_id):
        self.event_id = event_id

    def is_valid(self):
        return self.event_id is not None

class LibraryEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_registrations = db.relationship('EventRegistration', backref='library_event', lazy=True)

class EventRepository:
    def insert_event_registration(self, event_registration):
        if event_registration.is_valid():
            db.session.add(event_registration)
            db.session.commit()
        else:
            raise ValueError("Invalid event registration")

    def get_library_event(self, event_id):
        library_event = LibraryEvent.query.get(event_id)
        if library_event is None:
            raise ValueError("Library event not found")
        return library_event

    def update_library_event(self, library_event):
        existing_library_event = LibraryEvent.query.get(library_event.id).first()
        if existing_library_event is None:
            raise ValueError("Library event not found")
        db.session.add(library_event)
        db.session.commit()