

from flask import jsonify, request
from app.services.book_recommendation_service import generate_book_recommendations

@app.route('/book_recommendations', methods=['GET'])
def get_book_recommendations():
    patron_id = request.args.get('patron_id')
    recommended_books = generate_book_recommendations(patron_id)
    return jsonify(recommended_books)