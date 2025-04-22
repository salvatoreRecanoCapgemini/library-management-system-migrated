

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine('sqlite:///books.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    available_copies = Column(Integer)

Base.metadata.create_all(engine)

class BooksRepository:
    def update_book_availability(self, book_id, available_copies=None):
        try:
            if not isinstance(book_id, int) or (available_copies is not None and not isinstance(available_copies, int)):
                raise ValueError("Invalid input parameters")
            book = session.query(Books).filter_by(id=book_id).first()
            if book is None:
                raise ValueError("Book not found")
            if available_copies is not None:
                book.available_copies = available_copies
            else:
                book.available_copies += 1
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e