

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models import Book
import logging

class BookService:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def update_book_availability(self, book_id, change):
        try:
            if not isinstance(book_id, int) or not isinstance(change, int):
                raise ValueError('Invalid input type')
            book = self.session.query(Book).filter_by(book_id=book_id).first()
            if book:
                if book.available_copies + change < 0:
                    raise ValueError('Available copies cannot be negative')
                self.session.execute(text('CALL update_book_availability(:book_id, :change)'), {'book_id': book_id, 'change': change})
                self.session.commit()
            else:
                raise Exception('Book not found')
        except SQLAlchemyError as e:
            self.session.rollback()
            self.session.rollback()
            logging.error(f'Failed to update book availability: {e}')
            raise Exception('Failed to update book availability') from e
        except Exception as e:
            logging.error(f'Failed to update book availability: {e}')
            raise