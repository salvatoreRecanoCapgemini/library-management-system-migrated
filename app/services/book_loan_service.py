

from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, DatabaseError
from app.models import Book, Patron, Loan, db
import logging

MAX_LOANS = 5

def update_book_availability(book_id, quantity):
    try:
        book = Book.query.get(book_id)
        if book is None:
            raise ValueError("Book not found")
        book.available_copies += quantity
        db.session.commit()
    except DatabaseError as e:
        db.session.rollback()
        logging.error(f"Failed to update book availability: {e}")
        raise ValueError("Failed to update book availability")

def process_book_loan(patron_id, book_id, loan_days):
    if not isinstance(loan_days, int) or loan_days <= 0:
        raise ValueError("Invalid loan days")
    try:
        book = Book.query.get(book_id)
        if book is None:
            raise ValueError("Book not found")
        if book.available_copies <= 0:
            raise ValueError("Book is not available for loan")
        patron = Patron.query.get(patron_id)
        if patron is None:
            raise ValueError("Patron not found")
        if patron.status != 'ACTIVE':
            raise ValueError("Patron account is not active")
        if patron.loans.count() >= MAX_LOANS:
            raise ValueError("Patron has reached the maximum number of loans")
        existing_loan = Loan.query.filter_by(patron_id=patron_id, book_id=book_id, status='ACTIVE').first()
        if existing_loan is not None:
            raise ValueError("Patron has already borrowed the book")
        loan = Loan(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=loan_days), status='ACTIVE')
        db.session.add(loan)
        db.session.commit()
        update_book_availability(book_id, -1)
    except DatabaseError as e:
        db.session.rollback()
        logging.error(f"Failed to process book loan: {e}")
        raise ValueError("Failed to process book loan")