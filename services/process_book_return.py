

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Loans, Fines
from procedures import update_book_availability

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()

def process_book_return(p_loan_id):
    try:
        loan = session.query(Loans).filter_by(loan_id=p_loan_id).first()
        if loan is None or loan.status != 'ACTIVE':
            raise Exception('Loan does not exist or is not active')

        book_id = loan.book_id
        patron_id = loan.patron_id
        due_date = loan.due_date

        days_overdue = (date.today() - due_date).days
        if days_overdue > 0:
            fine_amount = days_overdue * 0.50
            fine = Fines(patron_id=patron_id, loan_id=p_loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today(), status='PENDING')
            session.add(fine)
            session.commit()
            if fine.id is None:
                raise Exception('Fine object not successfully inserted')
        else:
            session.commit()

        loan.status = 'RETURNED'
        session.commit()
        if loan.status != 'RETURNED':
            raise Exception('Loan status not successfully updated')

        update_book_availability(book_id, 1)
    except IntegrityError as e:
        session.rollback()
        raise Exception('Database integrity error: {}'.format(e))
    except Exception as e:
        session.rollback()
        raise Exception('Error processing book return: {}'.format(e))