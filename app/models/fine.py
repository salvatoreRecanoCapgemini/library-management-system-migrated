

from sqlalchemy import Column, Integer, DECIMAL, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    amount = Column(DECIMAL(10, 2))
    issue_date = Column(Date)
    due_date = Column(Date)
    fine_date = Column(Date)
    fine_amount = Column(DECIMAL(10, 2))
    payment_date = Column(Date)
    payment_amount = Column(DECIMAL(10, 2))
    status = Column(String, default='PENDING')

    patron = relationship('Patron', backref='fines')
    loan = relationship('Loan', backref='fine')
    audit_log = relationship('AuditLog', backref='fine')

    @classmethod
    def get_fines(cls, session, date_range):
        if not isinstance(date_range, tuple) or len(date_range) != 2:
            raise ValueError("Invalid date range")
        start_date, end_date = date_range
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError("Invalid date range")
        try:
            return session.query(cls).filter(cls.issue_date.between(start_date, end_date)).all()
        except Exception as e:
            raise Exception("Database error: " + str(e))