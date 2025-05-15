

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.loans import Loan
from models.reservations import Reservation
from datetime import timedelta

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

class LoanService:
    def extend_loan_period(self, loan_id, extension_days):
        if not isinstance(loan_id, int) or not isinstance(extension_days, int):
            raise ValueError('Invalid input parameters')
        if loan_id <= 0 or extension_days <= 0:
            raise ValueError('Invalid input parameters')
        try:
            session = Session()
            loan = session.query(Loan).filter_by(loan_id=loan_id).first()
            if loan is None:
                raise ValueError('Active loan not found')
            if not loan.is_active:
                raise ValueError('Loan is not active')
            if loan.extensions_count >= 2:
                raise ValueError('Maximum extensions reached')
            pending_reservations = session.query(Reservation).filter_by(book_id=loan.book_id, status='PENDING').all()
            if pending_reservations:
                raise ValueError('Book has pending reservations')
            loan.due_date += timedelta(days=extension_days)
            loan.extensions_count += 1
            session.commit()
        except Exception as e:
            session.rollback()
            raise e