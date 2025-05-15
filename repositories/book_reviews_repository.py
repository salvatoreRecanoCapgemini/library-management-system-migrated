

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class BookReviews(Base):
    __tablename__ = 'book_reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    patron_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)
    review_date = Column(DateTime, default=datetime.now)
    status = Column(Enum('PENDING', 'APPROVED', name='review_status'))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_book_review(book_id, patron_id, rating, review_text):
    if not all([isinstance(book_id, int), isinstance(patron_id, int), isinstance(rating, int), isinstance(review_text, str)]):
        raise ValueError('Invalid input parameters')
    if rating not in range(1, 6):
        raise ValueError('Invalid rating')
    if len(review_text) > 1000:
        raise ValueError('Review text is too long')

    try:
        new_review = BookReviews(book_id=book_id, patron_id=patron_id, rating=rating, review_text=review_text, status='PENDING')
        session.add(new_review)
        session.commit()
        return new_review.id
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        session.rollback()
        return str(e)
    finally:
        session.close()