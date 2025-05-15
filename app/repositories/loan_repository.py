

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    book_id = Column(Integer)
    loan_days = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class LoanRepository:
    def create_loan_record(self, patron_id, book_id, loan_days):
        if not isinstance(patron_id, int) or not isinstance(book_id, int) or not isinstance(loan_days, int):
            raise ValueError("Invalid input type")
        if patron_id <= 0 or book_id <= 0 or loan_days <= 0:
            raise ValueError("Invalid input value")
        try:
            loan = Loan(patron_id=patron_id, book_id=book_id, loan_days=loan_days, status='active')
            session.add(loan)
            session.commit()
            return loan.id
        except Exception as e:
            logging.error(f"Error creating loan record: {e}")
            session.rollback()
            raise

    def set_loan_status(self, loan_id, status):
        if not isinstance(loan_id, int) or not isinstance(status, str):
            raise ValueError("Invalid input type")
        if loan_id <= 0:
            raise ValueError("Invalid input value")
        if status not in ['active', 'inactive', 'returned']:
            raise ValueError("Invalid loan status")
        try:
            loan = session.query(Loan).filter_by(id=loan_id).first()
            if loan is None:
                raise ValueError("Loan not found")
            loan.status = status
            session.commit()
        except Exception as e:
            logging.error(f"Error setting loan status: {e}")
            session.rollback()
            raise