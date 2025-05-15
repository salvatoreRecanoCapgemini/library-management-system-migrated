

from datetime import datetime
from app.models import BookReview
from app import db

def add_book_review(book_id, patron_id, rating, review_text):
    if book_id is None or patron_id is None or rating is None or review_text is None:
        raise ValueError('Invalid input parameters')
    review = BookReview()
    review.book_id = book_id
    review.patron_id = patron_id
    review.rating = rating
    review.review_text = review_text
    review.review_date = datetime.now()
    review.status = 'PENDING'
    db.session.add(review)
    db.session.commit()
    return 'Review added successfully'