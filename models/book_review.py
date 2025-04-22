

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class BookReview(Base):
    __tablename__ = 'book_reviews'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    rating = Column(Integer)
    review_text = Column(String)
    review_date = Column(DateTime)
    status = Column(Enum('PENDING', 'APPROVED', 'REJECTED'))

    def __init__(self, book_id, patron_id, rating, review_text):
        if not isinstance(book_id, int) or not isinstance(patron_id, int) or not isinstance(rating, int):
            raise ValueError("Invalid input type")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(review_text, str):
            raise ValueError("Invalid input type")
        self.book_id = book_id
        self.patron_id = patron_id
        self.rating = rating
        self.review_text = review_text
        self.review_date = datetime.now()
        self.status = 'PENDING'