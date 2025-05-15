

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///books.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    available_copies = Column(Integer)

Base.metadata.create_all(engine)

class BookRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_books(self):
        try:
            book_data = self.db_session.query(Book).all()
            return book_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_book_by_id(self, book_id):
        if not isinstance(book_id, int) or book_id <= 0:
            return None
        try:
            book = self.db_session.query(Book).filter_by(id=book_id).first()
            return book
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def check_book_availability(self, book_id):
        if not isinstance(book_id, int) or book_id <= 0:
            return False
        try:
            book = self.get_book_by_id(book_id)
            if book and book.available_copies > 0:
                return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_book_availability(self, book_id, change):
        if not isinstance(book_id, int) or book_id <= 0:
            return False
        if not isinstance(change, int):
            return False
        try:
            book = self.get_book_by_id(book_id)
            if book:
                book.available_copies += change
                self.db_session.commit()
                return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def retrieve_book(self, book_id):
        if not isinstance(book_id, int) or book_id <= 0:
            return None
        try:
            book = self.get_book_by_id(book_id)
            return book
        except Exception as e:
            print(f"An error occurred: {e}")
            return None