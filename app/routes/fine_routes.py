

from flask import Blueprint, request, jsonify
from app.services.fine_service import FineService
import logging

fine_routes = Blueprint('fine_routes', __name__)

class FineRoutes:
    def __init__(self):
        self.fine_service = FineService()

    def process_fine_payment(self, fine_id, amount_paid):
        if not fine_id or not amount_paid:
            logging.error('Invalid input parameters')
            raise ValueError('Invalid input parameters')
        try:
            self.fine_service.process_fine_payment(fine_id, amount_paid)
        except Exception as e:
            logging.error(f'Error processing fine payment: {str(e)}')
            raise

@fine_routes.route('/fine/payment', methods=['POST'])
def handle_fine_payment():
    try:
        data = request.get_json()
        fine_id = data.get('fine_id')
        amount_paid = data.get('amount_paid')
        if not fine_id or not amount_paid:
            return jsonify({'message': 'Invalid input parameters'}), 400
        fine_routes_instance = FineRoutes()
        fine_routes_instance.process_fine_payment(fine_id, amount_paid)
        return jsonify({'message': 'Fine payment processed successfully'}), 200
    except Exception as e:
        logging.error(f'Error handling fine payment: {str(e)}')
        return jsonify({'message': 'Error processing fine payment'}), 500