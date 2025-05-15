

from app.services.loan_service import process_overdue_loans, extend_loan_period, process_book_return
from flask import request, jsonify, request

class LoanController:
    @app.route('/process_overdue_loans', methods=['POST'])
    def process_overdue_loans(self):
        try:
            process_overdue_loans()
            return jsonify({'message': 'Overdue loans processed successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400

    @app.route('/extend_loan_period', methods=['POST'])
    def extend_loan_period_endpoint(self):
        if 'p_loan_id' not in request.json:
            return jsonify({'message': 'Loan ID is required'}), 400
        p_loan_id = request.json['p_loan_id']
        p_extension_days = request.json.get('p_extension_days', 7)
        try:
            extend_loan_period(p_loan_id, p_extension_days)
            return jsonify({'message': 'Loan period extended successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400

    @app.route('/return_book', methods=['POST'])
    def return_book(self):
        if 'loan_id' not in request.json:
            return jsonify({'message': 'Loan ID is required'}), 400
        p_loan_id = request.json['loan_id']
        try:
            process_book_return(p_loan_id)
            return jsonify({'message': 'Book returned successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400