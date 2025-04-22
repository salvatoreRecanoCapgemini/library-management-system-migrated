

from flask import jsonify, request
from app.services.statistics_service import generate_monthly_statistics

class StatisticsController:
    def get_statistics(self):
        try:
            p_year = int(request.args.get('year'))
            p_month = int(request.args.get('month'))
            result = generate_monthly_statistics(p_year, p_month)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500