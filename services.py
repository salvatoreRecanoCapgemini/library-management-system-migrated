

from flask import current_app
from datetime import date, timedelta
from yourapplication import db
from yourapplication.models import Loans, Fines, Books

def process_book_return(loan_id):
    try:
        loan = Loans.query.get(loan_id)
        if loan is None or loan.status != 'ACTIVE':
            raise Exception('Loan not found or not active')

        overdue_days = (date.today() - loan.due_date).days

        if overdue_days > 0:
            fine_amount = overdue_days * 0.50
            fine = Fines(patron_id=loan.patron_id, loan_id=loan.loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today() + timedelta(days=30), status='PENDING')
            db.session.add(fine)

        loan.status = 'RETURNED'
        loan.return_date = date.today()

        db.session.commit()

        book = Books.query.get(loan.book_id)
        if book is not None:
            book.available_copies += 1
            book.status = 'AVAILABLE'
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error processing book return: {str(e)}')
        raise