

from datetime import date, timedelta
from app.repositories import loans_repository, books_repository
from app.db import db
import logging

class ProcessBookReturnService:
    def process_book_return(self, loan_id):
        try:
            loan = loans_repository.get_loan(loan_id)
            if not loan or loan.status != 'ACTIVE':
                raise Exception('Loan not found or not active')
            overdue_days = self.calculate_overdue_days(loan.due_date)
            if overdue_days > 0:
                fine_amount = self.calculate_fine_amount(overdue_days)
                loans_repository.create_fine_record(loan.patron_id, loan_id, fine_amount, date.today(), date.today() + timedelta(days=30))
            loans_repository.update_loan_status(loan_id, 'RETURNED')
            books_repository.update_book_availability(loan.book_id, loan.book.available_copies + 1)
            db.session.commit()
            logging.info(f'Book return processed successfully for loan id {loan_id}')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error processing book return for loan id {loan_id}: {str(e)}')
            raise

    def calculate_overdue_days(self, due_date):
        return (date.today() - due_date).days

    def calculate_fine_amount(self, overdue_days):
        fine_amount = overdue_days * 0.5  # implement fine amount calculation logic here
        return fine_amount