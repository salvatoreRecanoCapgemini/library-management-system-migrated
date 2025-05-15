

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import logging

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    loan_id = Column(Integer)
    fine_date = Column(DateTime)
    fine_amount = Column(Float)
    payment_date = Column(DateTime)
    payment_amount = Column(Float)
    status = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_fine(loan_id, due_date):
    if not isinstance(loan_id, int) or not isinstance(due_date, datetime.date):
        raise ValueError("Invalid input parameters")
    try:
        days_overdue = (datetime.date.today() - due_date).days
        fine_amount = max(0, days_overdue * 0.1)
        fine = Fine(loan_id=loan_id, fine_date=datetime.date.today(), fine_amount=fine_amount, status='PENDING')
        session.add(fine)
        session.commit()
    except Exception as e:
        logging.error(e)

def get_fines(start_date, end_date):
    if not isinstance(start_date, datetime.date) or not isinstance(end_date, datetime.date):
        raise ValueError("Invalid input parameters")
    try:
        fines = session.query(Fine).filter(Fine.fine_date.between(start_date, end_date)).all()
        return fines
    except Exception as e:
        logging.error(e)
        return []

def process_fine_payment(p_fine_id, p_amount_paid):
    if not isinstance(p_fine_id, int) or not isinstance(p_amount_paid, (int, float)) or p_amount_paid <= 0:
        raise ValueError("Invalid input parameters")
    try:
        fine = session.query(Fine).filter_by(fine_id=p_fine_id, status='PENDING').first()
        if fine is None:
            raise Exception('Valid unpaid fine not found')
        total_amount = fine.fine_amount
        if p_amount_paid < total_amount:
            raise Exception('Partial payments not supported')
        fine.status = 'PAID'
        fine.payment_date = datetime.date.today()
        fine.payment_amount = p_amount_paid
        session.commit()
    except Exception as e:
        logging.error(e)