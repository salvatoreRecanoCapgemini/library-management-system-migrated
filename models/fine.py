

from sqlalchemy import Column, Integer, ForeignKey, Date, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    amount = Column(DECIMAL(10, 2))
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)