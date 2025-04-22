

from flask_sqlalchemy import SQLAlchemy, db
from datetime import date

db = SQLAlchemy()

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, patron_id, book_id, loan_date, due_date, status, loan_id=None):
        if loan_id is not None:
            self.loan_id = loan_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.status = status

    def __repr__(self):
        return f'Loan(loan_id={self.loan_id if self.loan_id is not None else "None"}, patron_id={self.patron_id if self.patron_id is not None else "None"}, book_id={self.book_id if self.book_id is not None else "None"}, loan_date={self.loan_date if self.loan_date is not None else "None"}, due_date={self.due_date if self.due_date is not None else "None"}, status={self.status if self.status is not None else "None"})'