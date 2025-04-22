

from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'

    fine_id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    fine_amount = Column(Integer)
    paid_date = Column(Date)
    payment_status = Column(String)

    loan = relationship('Loan', backref='fines')