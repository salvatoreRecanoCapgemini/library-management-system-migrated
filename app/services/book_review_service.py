

from datetime import datetime
from app.models import BookReview
from app import db
import logging

class BookReviewService:
    def add_book_review(self, book_id, patron_id, rating, review_text):
        try:
            if not isinstance(book_id, int) or not isinstance(patron_id, int) or not isinstance(rating, int) or not isinstance(review_text, str):
                raise ValueError("Invalid input type")
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            review = BookReview(book_id, patron_id, rating, review_text)
            review.review_date = datetime.now()
            review.status = 'PENDING'
            db.session.add(review)
            db.session.commit()
            logging.info("Book review added successfully")
        except Exception as e:
            db.session.rollback()
            logging.error("Error adding book review: " + str(e))
            raise