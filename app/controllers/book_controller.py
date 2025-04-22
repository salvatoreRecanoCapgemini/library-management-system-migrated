

from flask import jsonify, request
from app.services.book_service import update_book_availability
import logging

def update_book_availability_controller():
    try:
        book_id = request.json.get('book_id')
        change = request.json.get('change')
        
        if not book_id or not change:
            return jsonify({"message": "Book ID and change are required"}), 400
        
        update_book_availability(book_id, change)
        return jsonify({"message": "Book availability updated successfully"}), 200
    except Exception as e:
        logging.error(str(e))
        return jsonify({"message": str(e)}), 500