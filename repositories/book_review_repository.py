

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from book_review import BookReview

class BookReviewRepository:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        self.db = scoped_session(sessionmaker(bind=engine))

    def add_book_review(self, book_review):
        """
        Adds a new book review to the database.

        Args:
            book_review (BookReview): The book review to add.

        Raises:
            ValueError: If the book review is None.
            Exception: If an error occurs during database operations.
        """
        if book_review is None:
            raise ValueError("Book review cannot be None")

        try:
            self.db.add(book_review)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception("Error adding book review: {}".format(str(e)))