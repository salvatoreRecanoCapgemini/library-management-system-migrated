

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from datetime import date
from flask import abort

db = SQLAlchemy()

class Patrons(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True)
    loans = relationship("Loans", backref="patron")
    fines = relationship("Fines", backref="patron")

class Loans(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    def __init__(self, book_id, patron_id, due_date, status):
        if not isinstance(book_id, int) or not isinstance(patron_id, int):
            abort(400, "Invalid book_id or patron_id")
        if not isinstance(due_date, date):
            abort(400, "Invalid due_date"))
        if not isinstance(status, str) or len(status) > 50:
            abort(400, "Invalid status")
        self.book_id = book_id
        self.patron_id = patron_id
        self.due_date = due_date
        self.status = status

class Fines(db.Model):
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'), primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.loan_id'), primary_key=True)
    amount = db.Column(db.Float)
    issue_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    def __init__(self, patron_id, loan_id, amount, issue_date, due_date, status):
        if not isinstance(patron_id, int) or not isinstance(loan_id, int):
            abort(400, "Invalid patron_id or loan_id")
        if not isinstance(amount, (int, float)):
            abort(400, "Invalid amount")
        if not isinstance(issue_date, date) or not isinstance(due_date, date):
            abort(400, "Invalid issue_date or due_date")
        if not isinstance(status, str) or len(status) > 50:
            abort(400, "Invalid status")
        self.patron_id = patron_id
        self.loan_id = loan_id
        self.amount = amount
        self.issue_date = issue_date
        self.due_date = due_date
        self.status = status

class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    available_copies = db.Column(db.Integer)
    loans = relationship("Loans", backref="book")

    def __init__(self, available_copies):
        if not isinstance(available_copies, int):
            abort(400, "Invalid available_copies")
        self.available_copies = available_copies

@event.listens_for(db.session, 'before_commit')
def receive_before_commit(session):
    for obj in session.new:
        if isinstance(obj, (Loans, Fines, Books)):
            try:
                session.add(obj)
            except SQLAlchemyError as e:
                session.rollback()
                abort(500, str(e))