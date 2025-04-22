

from flask import request, jsonify
from models.book_review import BookReview
from controllers.book_review_controller import BookReviewController
from app import db
from sqlalchemy.exc import IntegrityError
from flask_api import status

def validate_input(data):
    if 'book_id' not in data or 'patron_id' not in data or 'rating' not in data or 'review_text' not in data:
        return False
    return True

@app.route('/book-reviews', methods=['POST'])
def add_book_review():
    data = request.json
    if not validate_input(data):
        return jsonify({'message': 'Invalid input'}), status.HTTP_400_BAD_REQUEST

    book_id = data['book_id']
    patron_id = data['patron_id']
    rating = data['rating']
    review_text = data['review_text']

    if not BookReview.check_book_id_exists(book_id) or not BookReview.check_patron_id_exists(patron_id):
        return jsonify({'message': 'Book or patron not found'}), status.HTTP_404_NOT_FOUND

    review = BookReview(book_id, patron_id, rating, review_text)
    try:
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Book review added successfully'}), status.HTTP_201_CREATED
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to add book review'}), status.HTTP_500_INTERNAL_SERVER_ERROR