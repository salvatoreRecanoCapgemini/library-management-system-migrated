

from app import db
from datetime import date

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    loan_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    extensions_count = db.Column(db.Integer)

    book = db.relationship('Book', backref=db.backref('loans', lazy=True))

    def __init__(self, loan_id, patron_id, book_id, loan_date, due_date, status):
        if not isinstance(loan_id, int) or loan_id <= 0:
            raise ValueError("Invalid loan_id")
        if not isinstance(patron_id, int) or patron_id <= 0:
            raise ValueError("Invalid patron_id")
        if not isinstance(book_id, int) or book_id <= 0:
            raise ValueError("Invalid book_id")
        if not isinstance(loan_date, date):
            raise ValueError("Invalid loan_date")
        if not isinstance(due_date, date):
            raise ValueError("Invalid due_date")
        if not isinstance(status, str):
            raise ValueError("Invalid status")

        self.loan_id = loan_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.status = status
        self.extensions_count = 0

    def update_status(self, new_status):
        if not isinstance(new_status, str):
            raise ValueError("Invalid new_status")
        self.status = new_status

    def calculate_fine(self):
        fine_amount = 0
        if self.due_date < date.today():
            fine_amount = (date.today() - self.due_date).days * 0.5
            fine_amount *= (1 + self.extensions_count * 0.1)
        return fine_amount