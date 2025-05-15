

from flask import Blueprint, request, jsonify
from app.services.book_service import BookService

book_routes = Blueprint('book_routes', __name__)
book_service = BookService()

@book_routes.route('/update_availability', methods=['POST'])
def update_availability():
    try:
        data = request.get_json()
        if 'book_id' not in data or 'change_value' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400
        book_id = data['book_id']
        change_value = data['change_value']
        if not isinstance(book_id, int) or not isinstance(change_value, int):
            return jsonify({'error': 'Invalid data type'}), 400
        if not book_service.book_exists(book_id):
            return jsonify({'error': 'Book not found'}), 404
        book_service.update_availability(book_id, change_value)
        return jsonify({'message': 'Book availability updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500