

from app.services.book_loan_service import BookLoanService

class BookLoanController:
    def process_book_loan(self, p_patron_id, p_book_id, p_loan_days):
        if not isinstance(p_patron_id, int) or not isinstance(p_book_id, int) or not isinstance(p_loan_days, int):
            raise ValueError("Invalid input type")
        if p_patron_id <= 0 or p_book_id <= 0 or p_loan_days <= 0:
            raise ValueError("Invalid input value")
        try:
            book_loan_service = BookLoanService()
            book_loan_service.process_book_loan(p_patron_id, p_book_id, p_loan_days)
        except Exception as e:
            raise Exception("Failed to process book loan") from e