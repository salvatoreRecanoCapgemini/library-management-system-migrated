

from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BookReview(Base):
    __tablename__ = 'book_reviews'

    review_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    review_date = Column(Date)
    rating = Column(Float)

    book = relationship('Book', backref='reviews')
    patron = relationship('Patron', backref='reviews')