

from flask import Blueprint, request, jsonify
from app.services.statistics_service import StatisticsService
import logging
import datetime

statistics_controller = Blueprint('statistics_controller', __name__)

@statistics_controller.route('/statistics', methods=['GET'])
def get_statistics():
    try:
        p_year = request.args.get('year')
        p_month = request.args.get('month')
        
        if not p_year or not p_month:
            return jsonify({'error': 'Year and month parameters are required'}), 400
        
        try:
            p_year = int(p_year)
            p_month = int(p_month)
        except ValueError:
            return jsonify({'error': 'Year and month parameters must be integers'}), 400
        
        if not (1 <= p_month <= 12):
            return jsonify({'error': 'Month parameter must be between 1 and 12'}), 400
        
        try:
            statistics = StatisticsService.generate_monthly_statistics(p_year, p_month)
        except Exception as e:
            logging.error(f'Error generating statistics: {str(e)}')
            return jsonify({'error': 'Failed to generate statistics'}), 500
        
        if not statistics:
            return jsonify({'error': 'No data available for the specified period'}), 404
        
        return jsonify(statistics)
    except Exception as e:
        logging.error(f'Error handling request: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500