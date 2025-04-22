

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    payment_date = Column(DateTime)

engine = create_engine('sqlite:///fines.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = scoped_session(Session)

def get_fine_by_id(p_fine_id):
    fine = session.query(Fine).filter(Fine.id == p_fine_id, Fine.status == 'PENDING').first()
    if fine is None:
        raise Exception('Valid unpaid fine not found')
    return fine

def update_fine_status(p_fine_id, p_amount_paid):
    fine = get_fine_by_id(p_fine_id)
    remaining_amount = fine.amount - p_amount_paid
    if remaining_amount > 0:
        raise Exception('Partial payments not supported')
    elif remaining_amount < 0:
        raise Exception('Paid amount cannot be greater than the total amount')
    elif remaining_amount == 0:
        if fine.status == 'PAID':
            raise Exception('Fine is already paid')
        fine.status = 'PAID'
        fine.payment_date = datetime.now()
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
    return fine

def process_fine_payment(p_fine_id, p_amount_paid):
    fine = get_fine_by_id(p_fine_id)
    remaining_amount = fine.amount - p_amount_paid

    if remaining_amount < 0:
        raise Exception('Paid amount cannot be greater than the total amount')

    if remaining_amount == 0:
        if fine.status == 'PAID':
            raise Exception('Fine is already paid')
        fine.status = 'PAID'
        fine.payment_date = datetime.now()
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)