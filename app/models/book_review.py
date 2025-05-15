

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BookReview(Base):
    __tablename__ = 'book_reviews

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    rating = Column(Integer)
    review_text = Column(Text)
    review_date = Column(DateTime)
    status = Column(String)

    book = relationship('Book', backref='reviews')
    patron = relationship('Patron', backref='reviews')

    def __init__(self, review_id, patron_id, book_id, rating, review_text, review_date, status):
        if not isinstance(review_id, int) or not isinstance(patron_id, int) or not isinstance(book_id, int):
            raise ValueError("Review ID, Patron ID, and Book ID must be integers")
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if not isinstance(review_text, str):
            raise ValueError("Review text must be a string")
        if not isinstance(review_date, datetime):
            raise ValueError("Review date must be a datetime object")
        if not isinstance(status, str):
            raise ValueError("Status must be a string")

        self.id = review_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.rating = rating
        self.review_text = review_text
        self.review_date = review_date
        self.status = status