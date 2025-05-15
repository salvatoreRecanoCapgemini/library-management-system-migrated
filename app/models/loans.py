

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Loans(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(10), CheckConstraint("status IN ('ACTIVE', 'RETURNED')"))

    def __init__(self, book_id, patron_id, loan_date, due_date, status):
        if due_date < loan_date:
            raise ValueError("Due date cannot be earlier than loan date")
        if status not in ['ACTIVE', 'RETURNED']:
            raise ValueError("Invalid status")
        self.book_id = book_id
        self.patron_id = patron_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.status = status