

from flask import Blueprint, request, jsonify
from app.services import library_statistics_service

library_statistics_controller = Blueprint('library_statistics_controller', __name__)

@library_statistics_controller.route('/generate_monthly_statistics', methods=['GET'])
def generate_monthly_statistics():
    try:
        p_year = int(request.args.get('p_year'))
        p_month = int(request.args.get('p_month'))
        if not (1 <= p_month <= 12):
            return jsonify({'error': 'Invalid month'}), 400
        report_data = library_statistics_service.generate_monthly_statistics(p_year, p_month)
        if not report_data:
            return jsonify({'error': 'No data available'}), 404
        return jsonify(report_data)
    except ValueError:
        return jsonify({'error': 'Invalid year or month'}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500