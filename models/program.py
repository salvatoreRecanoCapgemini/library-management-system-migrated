

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Program(db.Model):
    program_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    min_participants = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    session_schedule = db.Column(db.JSON, nullable=False)