

from sqlalchemy import Column, Integer, Text, Timestamp, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class BookReview(Base):
    __tablename__ = 'book_reviews'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    patron_id = Column(Integer, ForeignKey('patrons.id'))
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    review_date = Column(Timestamp, nullable=False, default=datetime.utcnow)
    status = Column(Text, nullable=False, default='PENDING')

    book = relationship('Book', backref='reviews')
    patron = relationship('Patron', backref='reviews')

    def validate(self):
        if not self.book_id or not self.patron_id or not self.rating or not self.review_text:
            return False
        if len(self.review_text) > 500:
            return False
        if self.rating < 1 or self.rating > 5:
            return False
        if self.status != 'PENDING':
            return False
        return True