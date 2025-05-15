

from flask import request, jsonify
from app.services.book_loan_service import BookLoanService
import logging

class BookLoanController:
    def __init__(self):
        self.book_loan_service = BookLoanService()
        self.logger = logging.getLogger(__name__)

    def book_loan_request(self):
        try:
            patron_id = request.args.get('patron_id')
            book_id = request.args.get('book_id')
            loan_days = request.args.get('loan_days', default=14, type=int)

            if not patron_id or not book_id:
                self.logger.error('Missing required arguments: patron_id and book_id')
                return jsonify({'error': 'Missing required arguments: patron_id and book_id'}), 400

            if loan_days <= 0:
                self.logger.error('Invalid loan days: must be a positive integer')
                return jsonify({'error': 'Invalid loan days: must be a positive integer'}), 400

            self.book_loan_service.process_book_loan(patron_id, book_id, loan_days)
            self.logger.info('Book loan request processed successfully')
            return jsonify({'message': 'Book loan request processed successfully'}), 200
        except Exception as e:
            self.logger.error(f'Error processing book loan request: {str(e)}')
            return jsonify({'error': 'Error processing book loan request'}), 500