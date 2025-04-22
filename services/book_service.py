

from models.book import Book
from sqlalchemy.orm import sessionmaker

class BookService:
    def __init__(self, session):
        self.session = session

    def update_availability(self, book_id, change):
        book = self.session.query(Book).filter_by(book_id=book_id).first()
        if book:
            book.available_copies += change
            self.session.commit()
        else:
            raise ValueError('Book not found')