

from datetime import date
from sqlalchemy import Column, Integer, Date, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.patron import Patron
from app.models.book import Book
from app.models.fine import Fine

Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    loan_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date)
    fine_amount = Column(Float)
    status = Column(String(50))
    patron = relationship('Patron', backref='loans')
    book = relationship('Book', backref='loans')
    fine = relationship('Fine', backref='loans')

    def __init__(self, loan_id, patron_id, book_id, loan_date, due_date, return_date, fine_amount, status):
        if not isinstance(loan_id, int) or not isinstance(patron_id, int) or not isinstance(book_id, int):
            raise ValueError("loan_id, patron_id, and book_id must be integers")
        if not isinstance(loan_date, date) or not isinstance(due_date, date) or not isinstance(return_date, date):
            raise ValueError("loan_date, due_date, and return_date must be dates")
        if not isinstance(fine_amount, float):
            raise ValueError("fine_amount must be a float")
        if not isinstance(status, str):
            raise ValueError("status must be a string")
        self.loan_id = loan_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date
        self.fine_amount = fine_amount
        self.status = status

    @classmethod
    def get_loans(cls, date_range=None):
        if date_range is None:
            return cls.query.all()
        start_date, end_date = date_range
        return cls.query.filter(cls.loan_date >= start_date, cls.loan_date <= end_date).all()