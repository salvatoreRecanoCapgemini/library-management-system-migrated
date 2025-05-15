

from flask import jsonify
from app.services.book_service import BookService

class BookController:
    def update_book_availability(self, book_id, change):
        book_service = BookService()
        book_service.update_book_availability(book_id, change)
        return jsonify({'message': 'Book availability updated successfully'})