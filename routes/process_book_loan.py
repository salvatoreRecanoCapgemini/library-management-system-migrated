

from flask import Blueprint, request, jsonify
from datetime import date, timedelta
from yourapplication import db
from yourapplication.models import Books, Patrons, Loans
import logging

process_book_loan_blueprint = Blueprint('process_book_loan', __name__)

@process_book_loan_blueprint.route('/process_book_loan', methods=['POST'])
def process_book_loan():
    try:
        patron_id = request.json['patron_id']
        book_id = request.json['book_id']
        loan_days = request.json['loan_days']

        if not isinstance(loan_days, int) or loan_days <= 0:
            return jsonify({'error': 'Loan days must be a positive integer'}), 400

        patron = Patrons.query.get(patron_id)
        if patron is None:
            return jsonify({'error': 'Patron not found'}), 404

        book = Books.query.get(book_id)
        if book is None:
            return jsonify({'error': 'Book not found'}), 404

        available_copies = book.available_copies
        if available_copies <= 0:
            return jsonify({'error': 'Book is not available for loan'}), 400

        patron_status, active_loans = patron.status, patron.active_loans
        if patron_status != 'ACTIVE':
            return jsonify({'error': 'Patron account is not active'}), 400
        if active_loans >= 5:
            return jsonify({'error': 'Patron has reached maximum number of loans'}), 400

        loan = Loans(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=loan_days))
        db.session.add(loan)
        db.session.commit()

        book.available_copies -= 1
        db.session.commit()

        return jsonify({'message': 'Loan created successfully'}), 201
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500