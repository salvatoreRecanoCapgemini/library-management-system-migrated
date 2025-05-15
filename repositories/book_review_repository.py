

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BookReview
from datetime import datetime

class BookReviewRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_book_reviews(self):
        try:
            book_review_data = self.Session().query(BookReview).all()
            return book_review_data
        except Exception as e:
            raise Exception("Failed to retrieve book reviews: " + str(e))

    def add_book_review(self, book_id, patron_id, rating, review_text):
        if book_id is None or patron_id is None or rating is None or review_text is None:
            raise ValueError("Invalid input parameters")

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        review = BookReview()
        review.book_id = book_id
        review.patron_id = patron_id
        review.rating = rating
        review.review_text = review_text
        review.review_date = datetime.now()
        review.status = 'PENDING'

        try:
            session = self.Session()
            session.add(review)
            session.commit()
            return review.id
        except Exception as e:
            raise Exception("Failed to add book review: " + str(e))