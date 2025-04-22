

from flask import Blueprint, request, jsonify
from app.services.loan_service import process_overdue_loans, extend_loan_period, process_book_return
from app.models.loan import Loan

loan_controller = Blueprint('loan_controller', __name__)

@loan_controller.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return jsonify([loan.to_dict() for loan in loans])

@loan_controller.route('/loans/process_overdue', methods=['POST'])
def process_overdue_loans():
    try:
        process_overdue_loans()
        return jsonify({'message': 'Overdue loans processed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_controller.route('/loans/extend_period', methods=['POST'])
def extend_loan_period_request():
    if 'loan_id' not in request.json or 'extension_days' not in request.json:
        return jsonify({'error': 'loan_id and extension_days are required'}), 400
    p_loan_id = request.json['loan_id']
    p_extension_days = request.json['extension_days']
    try:
        extend_loan_period(p_loan_id, p_extension_days)
        return jsonify({'message': 'Loan period extended successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_controller.route('/return_book', methods=['POST'])
def return_book():
    if 'loan_id' not in request.json:
        return jsonify({'error': 'loan_id is required'}), 400
    loan_id = request.json['loan_id']
    try:
        process_book_return(loan_id)
        return jsonify({'message': 'Book returned successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400