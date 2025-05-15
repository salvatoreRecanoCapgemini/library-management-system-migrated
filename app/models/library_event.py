

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class LibraryEvent(db.Model):
    __tablename__ = 'library_events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    event_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer)

    def __init__(self, title, event_date, status, max_participants, current_participants=0):
        self.title = title
        self.event_date = event_date
        self.status = status
        self.max_participants = max_participants
        self.current_participants = current_participants