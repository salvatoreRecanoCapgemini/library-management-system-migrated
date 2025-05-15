

from flask import request, jsonify
from app import db
from app.models import Book, Patron, BookReview
from datetime import datetime

@app.route('/book_reviews', methods=['POST'])
def add_book_review():
    data = request.get_json()
    book_id = data.get('book_id')
    patron_id = data.get('patron_id')
    rating = data.get('rating')
    review_text = data.get('review_text')

    if not all([book_id, patron_id, rating, review_text]):
        return jsonify({'error': 'Invalid input parameters'}), 400

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'error': 'Invalid rating'}), 400

    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    patron = Patron.query.get(patron_id)
    if patron is None:
        return jsonify({'error': 'Patron not found'}), 404

    try:
        review = BookReview(book_id=book_id, patron_id=patron_id, rating=rating, review_text=review_text, review_date=datetime.now(), status='PENDING')
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review added successfully', 'review_id': review.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add review'}), 500