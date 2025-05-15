

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.loans import Loans
from models.reservations import Reservations
import logging
from datetime import datetime, timedelta

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()

def extend_loan_period(p_loan_id, p_extension_days):
    try:
        if not isinstance(p_loan_id, int) or not isinstance(p_extension_days, int):
            raise Exception('Invalid input parameters')
        if p_extension_days <= 0:
            raise Exception('Extension days must be a positive integer')
        loan_details = session.query(Loans).filter_by(loan_id=p_loan_id, status='ACTIVE').first()
        if loan_details is None:
            raise Exception('Active loan not found')
        if loan_details.extensions_count >= 2:
            raise Exception('Maximum extensions reached')
        if loan_details.due_date < datetime.now():
            raise Exception('Loan due date is in the past')
        pending_reservations = session.query(Reservations).filter_by(book_id=loan_details.book_id, status='PENDING').first()
        if pending_reservations is not None:
            raise Exception('Book has pending reservations')
        new_due_date = loan_details.due_date + timedelta(days=p_extension_days)
        loan_details.due_date = new_due_date
        loan_details.extensions_count += 1
        session.commit()
    except Exception as e:
        logging.error(f'Error extending loan period: {str(e)}')
        session.rollback()
        raise