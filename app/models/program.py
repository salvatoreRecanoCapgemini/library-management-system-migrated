

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Program(db.Model):
    __tablename__ = 'programs'
    program_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    min_participants = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    session_schedule = db.Column(db.JSONB, nullable=False)
    registrations = db.relationship('Registration', backref='program', lazy=True)

    def __init__(self, program_id, name, status, min_participants, cost, session_schedule):
        self.program_id = program_id
        self.name = name
        self.status = status
        self.min_participants = min_participants
        self.cost = cost
        self.session_schedule = session_schedule

    def update_status(self, status):
        self.status = status

    def update_attendance_records(self, attendance_records):
        # Update attendance records for program
        for record in attendance_records:
            registration = Registration.query.filter_by(program_id=self.program_id, attendee_id=record['attendee_id']).first()
            if registration:
                registration.attendance = record['attendance']

    def start_program(self):
        if self.status != 'PUBLISHED':
            raise ValueError('Program is not in the PUBLISHED status')
        if self.min_participants > 0 and self.get_registration_count() < self.min_participants:
            create_waitlist_notification_batch(self.program_id)
            self.status = 'CANCELLED'
        else:
            self.session_schedule = initialize_session_schedule(self.program_id)
            self.status = 'IN_PROGRESS'

    def calculate_metrics(self):
        metrics = {}
        metrics['total_registrations'] = self.get_total_registrations()
        metrics['total_attendees'] = self.get_total_attendees()
        metrics['total_revenue'] = self.get_total_revenue()
        metrics['average_attendance_rate'] = self.get_average_attendance_rate()
        return metrics

    def get_registration_count(self):
        return len(self.registrations)

    def get_total_registrations(self):
        return len(self.registrations)

    def get_total_attendees(self):
        attendees = 0
        for registration in self.registrations:
            if registration.attendance:
                attendees += 1
        return attendees

    def get_total_revenue(self):
        return self.cost * len(self.registrations)

    def get_average_attendance_rate(self):
        if len(self.registrations) == 0:
            return 0
        attendees = 0
        for registration in self.registrations:
            if registration.attendance:
                attendees += 1
        return attendees / len(self.registrations)

def create_waitlist_notification_batch(program_id):
    # Create a waitlist notification batch
    pass

def initialize_session_schedule(program_id):
    # Initialize the session schedule
    pass