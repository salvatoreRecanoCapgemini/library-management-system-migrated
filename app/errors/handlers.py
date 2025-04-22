

from sqlalchemy.exc import IntegrityError, DatabaseError
from flask import jsonify
import logging

def handle_integrity_error(e):
    logging.error('Integrity error: %s', e)
    return jsonify({'error': 'Integrity error'}), 400

def handle_database_error(e):
    logging.error('Database error: %s', e)
    return jsonify({'error': 'Database error'}), 500

def patron_service_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            return handle_integrity_error(e)
        except DatabaseError as e:
            return handle_database_error(e)
    return wrapper

@patron_service_error_handler
def patron_service_function():
    # PatronService functionality
    pass