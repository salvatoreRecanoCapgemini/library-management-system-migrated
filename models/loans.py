

from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Loans(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    loan_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)
    extensions_count = Column(Integer)

    book = relationship('Books', backref='loans')
    patron = relationship('Patrons', backref='loans')