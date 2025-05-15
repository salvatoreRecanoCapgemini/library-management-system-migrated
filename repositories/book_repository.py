

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import logging

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publication_date = Column(DateTime)
    available_copies = Column(Integer)
    total_copies = Column(Integer)
    average_rating = Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class BookRepository:
    def __init__(self, db_session):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)

    def get_books(self, date_range):
        try:
            if not isinstance(date_range, tuple) or len(date_range) != 2:
                self.logger.error('Invalid date range')
                raise ValueError('Invalid date range')

            books = self.db_session.query(Book).filter(Book.publication_date.between(date_range[0], date_range[1])).all()
            return books

        except Exception as e:
            self.logger.error(f'Error getting books: {e}')
            raise e

    def update_book_availability(self, book_id, change_value):
        try:
            if not isinstance(book_id, int) or not isinstance(change_value, int):
                self.logger.error('Invalid book ID or change value')
                raise ValueError('Invalid book ID or change value')

            book = self.db_session.query(Book).filter_by(book_id=book_id).first()

            if not book:
                self.logger.error('Book not found')
                raise ValueError('Book not found')

            book.available_copies += change_value
            self.db_session.commit()

        except IntegrityError as e:
            self.db_session.rollback()
            self.logger.error(f'Integrity error: {e}')
            raise e

        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f'Error updating book availability: {e}')
            raise e