

from app.services.fine_service import FineService
from flask import jsonify
import logging

class FineController:
    def __init__(self):
        self.fine_service = FineService()
        self.logger = logging.getLogger(__name__)

    def handle_fine_payment_request(self, fine_id, amount_paid):
        if not isinstance(fine_id, int) or not isinstance(amount_paid, (int, float)):
            return jsonify({'error': 'Invalid input type'}), 400

        try:
            self.fine_service.process_fine_payment(fine_id, amount_paid)
            return jsonify({'message': 'Fine payment processed successfully'})
        except ValueError as e:
            self.logger.error(f'Invalid input: {str(e)}')
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            self.logger.error(f'An error occurred: {str(e)}')
            return jsonify({'error': 'An unexpected error occurred'}), 500