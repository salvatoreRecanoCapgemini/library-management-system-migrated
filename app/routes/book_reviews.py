

from flask import request, jsonify
from app.models.book_review import BookReview
from app import db
from datetime import datetime
import logging

@app.route('/book_reviews', methods=['POST'])
def add_book_review():
    book_id = request.json.get('book_id')
    patron_id = request.json.get('patron_id')
    rating = request.json.get('rating')
    review_text = request.json.get('review_text')

    if not all([book_id, patron_id, rating, review_text]) or not all([book_id.strip(), patron_id.strip(), rating.strip(), review_text.strip()]):
        return jsonify({'error': 'Invalid input parameters'}), 400

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'error': 'Invalid rating'}), 400

    review = BookReview(book_id=book_id, patron_id=patron_id, rating=rating, review_text=review_text)
    review.review_date = datetime.now()
    review.status = 'PENDING'

    try:
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review added successfully', 'review_id': review.id}), 201
    except Exception as e:
        logging.error(f"Error adding review: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to add review'}), 500