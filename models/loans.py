

from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    due_date = Column(Date)
    status = Column(String)
    loan_date = Column(Date)
    return_date = Column(Date)
    extensions_count = Column(Integer)

    patron = relationship('Patron', backref='loans')
    book = relationship('Book', backref='loans')