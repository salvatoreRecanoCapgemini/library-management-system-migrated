

from sqlalchemy import Column, Integer, Date, String, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Fines(Base):
    __tablename__ = 'fines'
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    amount = Column(DECIMAL(10, 2))
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)

    patron = relationship('Patrons', backref='fines')
    loan = relationship('Loans', backref='fines')