

from flask import current_app
from app import db
from app.models import Book

class BookService:
    def update_book_availability(self, book_id, change):
        if not isinstance(book_id, int):
            raise ValueError('Book ID must be an integer')
        if not isinstance(change, int):
            raise ValueError('Change value must be an integer')
        if change < 0:
            raise ValueError('Change value must be a non-negative integer')
        try:
            book = Book.query.get(book_id)
            if book:
                book.available_copies += change
                db.session.commit()
            else:
                raise Exception('Book not found')
        finally:
            db.session.close()