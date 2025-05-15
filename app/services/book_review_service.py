

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class BookReviewStatus(PyEnum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class BookReview(Base):
    __tablename__ = 'book_reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    patron_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)
    review_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Enum(BookReviewStatus), default=BookReviewStatus.PENDING, nullable=False)

class BookReviewService:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_book_review(self, book_id, patron_id, rating, review_text):
        try:
            if not all([book_id, patron_id, rating, review_text]):
                return {'error': 'Invalid input parameters'}
            if not isinstance(book_id, int) or not isinstance(patron_id, int) or not isinstance(rating, int):
                return {'error': 'Invalid input parameters'}
            if rating < 1 or rating > 5:
                return {'error': 'Invalid rating'}
            review = BookReview(book_id=book_id, patron_id=patron_id, rating=rating, review_text=review_text)
            self.session.begin()
            self.session.add(review)
            self.session.commit()
            return {'id': review.id}
        except Exception as e:
            self.session.rollback()
            return {'error': str(e)}