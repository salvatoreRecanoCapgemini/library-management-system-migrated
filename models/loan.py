

from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from models.reservation import Reservation

Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    due_date = Column(Date)
    status = Column(String)
    extensions_count = Column(Integer)

    MAX_EXTENSIONS = 2
    DEFAULT_EXTENSION_DAYS = 7

    patron = relationship("Patron", backref="loans")
    book = relationship("Book", backref="loans")

    def __init__(self, patron_id, book_id, due_date, status):
        self.patron_id = patron_id
        self.book_id = book_id
        self.due_date = due_date
        self.status = status
        self.extensions_count = 0

    def extend_loan_period(self, p_extension_days, db):
        if self.status != 'ACTIVE':
            raise ValueError('Active loan not found')
        if self.extensions_count >= self.MAX_EXTENSIONS:
            raise ValueError('Maximum extensions reached')
        reservation = db.query(Reservation).filter_by(book_id=self.book_id, status='PENDING').first()
        if reservation:
            raise ValueError('Book has pending reservations')
        self.due_date += p_extension_days
        self.extensions_count += 1
        db.session.add(self)
        db.session.commit()