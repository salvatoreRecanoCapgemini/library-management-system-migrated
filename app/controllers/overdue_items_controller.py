

from flask import Blueprint, request, jsonify
from app.services.overdue_items_service import OverdueItemsService
import logging

overdue_items_controller = Blueprint('overdue_items_controller', __name__)

@overdue_items_controller.route('/process_overdue_items', methods=['POST'])
def process_overdue_items():
    try:
        if not request.is_json:
            return jsonify({'error': 'Invalid request, JSON expected'}), 400

        result = OverdueItemsService.process_overdue_items()
        if result is None:
            return jsonify({'error': 'Invalid result from OverdueItemsService'}), 500

        return jsonify({'result': result}), 200
    except Exception as e:
        logging.error(f'Error processing overdue items: {str(e)}')
        return jsonify({'error': str(e)}), 500