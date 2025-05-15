

from datetime import datetime, date
from app.repositories import LoansRepository, FinesRepository, BooksRepository

class BookReturnService:
    def __init__(self, loans_repository, fines_repository, books_repository):
        self.loans_repository = loans_repository
        self.fines_repository = fines_repository
        self.books_repository = books_repository
        self.fine_per_day = 0.10

    def process_book_return(self, loan_id):
        loan_details = self.loans_repository.retrieve_loan_details(loan_id)
        if loan_details is None or loan_details.status != 'ACTIVE':
            raise Exception('Active loan not found')
        book_id = loan_details.book_id
        patron_id = loan_details.patron_id
        due_date = loan_details.due_date
        days_overdue = self.calculate_days_overdue(due_date)
        if days_overdue > 0:
            fine_amount = self.calculate_fine_amount(days_overdue)
            fine = self.create_fine_object(patron_id, loan_id, fine_amount, due_date)
            self.fines_repository.insert_fine(fine)
        self.loans_repository.update_loan_status(loan_id, 'RETURNED')
        self.books_repository.update_book_availability(book_id, 1)

    def calculate_days_overdue(self, due_date):
        today = datetime.now().date()
        return (today - due_date).days

    def calculate_fine_amount(self, days_overdue):
        return days_overdue * self.fine_per_day

    def create_fine_object(self, patron_id, loan_id, fine_amount, due_date):
        if not patron_id or not loan_id or fine_amount < 0 or not due_date:
            raise Exception('Invalid fine object parameters')
        return {
            'patron_id': patron_id,
            'loan_id': loan_id,
            'fine_amount': fine_amount,
            'due_date': due_date
        }

def get_book_return_service(loans_repository, fines_repository, books_repository):
    return BookReturnService(loans_repository, fines_repository, books_repository)