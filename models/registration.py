

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registration(db.Model):
    registration_id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.program_id'), nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    attendance_log = db.Column(db.JSON, nullable=False)