

from flask import jsonify
from app.services.book_service import BookService
import logging

class BookController:
    def update_book_availability(self, book_id, change_value):
        try:
            if not isinstance(book_id, int) or not isinstance(change_value, int):
                raise ValueError("Invalid input type")
            if book_id <= 0 or change_value < 0:
                raise ValueError("Invalid input value")
            book_service = BookService()
            book_service.update_book_availability(book_id, change_value)
            return jsonify({'message': 'Book availability updated successfully'})
        except ValueError as e:
            logging.error(f"Error updating book availability: {str(e)}")
            return jsonify({'error': str(e)})
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'})