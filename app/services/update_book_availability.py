

from app import db
from app.models import Books
import logging

def update_book_availability(book_id, increment):
    if increment < 0:
        raise ValueError('Invalid increment value')
    try:
        book = Books.query.get(book_id)
        if book is None:
            raise ValueError('Book not found')
        book.available_copies += increment
        db.session.commit()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        db.session.rollback()
        raise