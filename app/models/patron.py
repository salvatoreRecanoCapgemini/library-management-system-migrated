

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patron(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    reading_history = db.Column(db.List(db.Integer))
    preferences = db.Column(db.List(db.String))
    status = db.Column(db.String)
    active_loans = db.Column(db.Integer)
    phone = db.Column(db.String)
    membership_date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    birth_date = db.Column(db.Date, nullable=False)

    def __init__(self, patron_id, email, first_name, last_name, reading_history, preferences, status, active_loans, phone, membership_date=None, birth_date=None):
        self.patron_id = patron_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.reading_history = reading_history
        self.preferences = preferences
        self.status = status
        self.active_loans = active_loans
        self.phone = phone
        if membership_date is None:
            self.membership_date = db.func.current_date()
        else:
            self.membership_date = membership_date
        if birth_date is None:
            raise ValueError("Birth date is required")
        else:
            self.birth_date = birth_date

    def __repr__(self):
        return f"Patron('{self.first_name}', '{self.last_name}', '{self.email}', '{self.patron_id}', '{self.reading_history}', '{self.preferences}', '{self.status}', '{self.active_loans}', '{self.phone}', '{self.membership_date}', '{self.birth_date}')"

    def get_reading_history(self):
        return db.session.query(Patron.reading_history).filter(Patron.patron_id == self.patron_id).first()

    def get_preferences(self):
        return db.session.query(Patron.preferences).filter(Patron.patron_id == self.patron_id).first()