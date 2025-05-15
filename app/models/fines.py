

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Fines(db.Model):
    fine_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'))
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.loan_id'))
    amount = db.Column(db.DECIMAL)
    issue_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(10))
    fine_amount = db.Column(db.DECIMAL, nullable=False)
    paid_amount = db.Column(db.DECIMAL, nullable=False)
    payment_date = db.Column(db.Date)

    __table_args__ = (
        CheckConstraint(status.in_(['ACTIVE', 'PAID'])),
        {}
    )