

from datetime import datetime, date
from app import db
from app.models import Loans, Fines
from app.services import update_book_availability
import logging

def calculate_days_overdue(due_date):
    today = datetime.now()
    due_date = datetime.combine(due_date.year, due_date.month, due_date.day)
    return (today - due_date).days

def calculate_fine_amount(days_overdue, fine_rate=0.25):
    fine_amount = fine_rate * days_overdue
    return fine_amount

def process_book_return(loan_id):
    try:
        loan_details = Loans.query.get(loan_id)
        if loan_details is None or loan_details.status != 'ACTIVE':
            raise Exception('Active loan not found')
        book_id = loan_details.book_id
        patron_id = loan_details.patron_id
        due_date = loan_details.due_date
        days_overdue = calculate_days_overdue(due_date)
        if days_overdue > 0:
            fine_amount = calculate_fine_amount(days_overdue)
            fine = Fines(patron_id=patron_id, loan_id=loan_id, amount=fine_amount, issue_date=due_date, due_date=due_date, status='ACTIVE')
            db.session.add(fine)
        loan_details.status = 'RETURNED'
        db.session.commit()
        update_book_availability(book_id, 1)
    except Exception as e:
        logging.error(f"Error processing book return: {e}")
        db.session.rollback()
        raise