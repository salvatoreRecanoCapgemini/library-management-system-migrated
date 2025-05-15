

package app.controllers

import app.services.BookLoanService
import logging

class BookLoanController:
    def handle_book_loan_request(self, patron_id, book_id, loan_days):
        if not all([patron_id, book_id, loan_days]):
            raise ValueError("patron_id, book_id, and loan_days are required")

        book_loan_service = BookLoanService()
        try:
            result = book_loan_service.process_book_loan(patron_id, book_id, loan_days)
            if result is None:
                raise ValueError("Book loan service did not return a value")
        except ValueError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise