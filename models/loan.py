

package models

class Loan:
    def __init__(self, loan_id: int, patron_id: int, book_id: int, loan_date: str):
        if not isinstance(loan_id, int) or not isinstance(patron_id, int) or not isinstance(book_id, int):
            raise ValueError("loan_id, patron_id, and book_id must be integers")
        if not isinstance(loan_date, str):
            raise ValueError("loan_date must be a string")
        self.loan_id = loan_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.loan_date = loan_date