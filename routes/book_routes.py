

from flask import request, jsonify
from services.book_service import BookService
from database import session

def book_routes(app):
    @app.route('/books/<int:book_id>/availability', methods=['PATCH'])
    def update_availability(book_id):
        try:
            change = request.json['change']
            book_service = BookService(session)
            book_service.update_availability(book_id, change)
            return jsonify({'message': 'Book availability updated successfully'})
        except KeyError as e:
            return jsonify({'error': 'Missing required parameter'}), 400
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500