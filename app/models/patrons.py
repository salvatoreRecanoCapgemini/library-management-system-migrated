

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patrons(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    active_loans = db.Column(db.Integer)