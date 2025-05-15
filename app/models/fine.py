

from app import db
from sqlalchemy import DECIMAL, Date
from sqlalchemy.exc import IntegrityError

class Fine(db.Model):
    fine_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, nullable=False)
    loan_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(DECIMAL(10, 2), nullable=False)
    issue_date = db.Column(Date, nullable=False)
    due_date = db.Column(Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(Date, nullable=True)

    def __init__(self, fine_id, patron_id, loan_id, amount, issue_date, due_date, status, payment_date=None):
        self.fine_id = fine_id
        self.patron_id = patron_id
        self.loan_id = loan_id
        self.amount = amount
        self.issue_date = issue_date
        self.due_date = due_date
        self.status = status
        self.payment_date = payment_date

    def create_fine_record(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Failed to create fine record: {}".format(e))

    def update_fine_status(self, status):
        if not isinstance(status, str):
            raise ValueError("Status must be a string")
        self.status = status
        db.session.commit()