

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Loan, Reservation
from datetime import timedelta

MAX_EXTENSIONS = 2
DEFAULT_EXTENSION_DAYS = 7

def extend_loan_period(p_loan_id, p_extension_days=DEFAULT_EXTENSION_DAYS):
    engine = create_engine('postgresql://user:password@host:port/dbname')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        loan = retrieve_loan_details(p_loan_id, session)

        if loan is None:
            raise ValueError('Loan not found')

        if loan.status != 'ACTIVE':
            raise ValueError('Active loan not found')

        if loan.extensions_count >= MAX_EXTENSIONS:
            raise ValueError('Maximum extensions reached')

        reservation = retrieve_reservation(loan.book_id, session)
        if reservation and reservation.status == 'PENDING':
            raise ValueError('Book has pending reservations')

        loan.due_date += timedelta(days=p_extension_days)
        loan.extensions_count += 1

        commit_changes(session)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def retrieve_loan_details(p_loan_id, session):
    loan = session.query(Loan).filter_by(id=p_loan_id, status='ACTIVE').first()
    return loan

def retrieve_reservation(p_book_id, session):
    reservation = session.query(Reservation).filter_by(book_id=p_book_id, status='PENDING').first()
    return reservation

def commit_changes(session):
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e