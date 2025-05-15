

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registration(db.Model):
    __tablename__ = 'registrations'
    registration_id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'), nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'), nullable=False)
    payment_status = db.Column(db.String(100), nullable=False)
    attendance_log = db.Column(db.JSONB, nullable=False)
    program = db.relationship('Program', backref='registrations', lazy=True)
    patron = db.relationship('Patron', backref='registrations', lazy=True)

    def __init__(self, registration_id, program_id, patron_id, payment_status, attendance_log):
        self.registration_id = registration_id
        self.program_id = program_id
        self.patron_id = patron_id
        self.payment_status = payment_status
        self.attendance_log = attendance_log

    def update_attendance_log(self, attendance_record):
        self.attendance_log.append(attendance_record)

    def calculate_metrics(self):
        metrics = {}
        metrics['attendance_log'] = self.attendance_log
        return metrics