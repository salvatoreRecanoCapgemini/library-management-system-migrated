

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

engine = create_engine('sqlite:///books.db')
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    available_copies = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class BookRepository:
    def get_book_availability(self, book_id):
        try:
            book = session.query(Book).filter_by(id=book_id).first()
            if book is None:
                logging.error(f"Book with id {book_id} does not exist in the database")
                return None
            return book.available_copies
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def update_book_availability(self, book_id, change_value):
        try:
            if change_value < 0:
                logging.error("Change value cannot be negative")
                return
            book = session.query(Book).filter_by(id=book_id).first()
            if book is None:
                logging.error(f"Book with id {book_id} does not exist in the database")
                return
            book.available_copies += change_value
            session.commit()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            session.rollback()