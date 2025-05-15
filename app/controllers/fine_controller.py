

from flask import Blueprint, request
from app.services.fine_service import process_fine_payment

fine_controller = Blueprint('fine_controller', __name__)

@fine_controller.route('/fine/payment', methods=['POST'])
def handle_fine_payment():
    p_fine_id = request.json['fine_id']
    p_amount_paid = request.json['amount_paid']
    process_fine_payment(p_fine_id, p_amount_paid)
    return 'Fine payment processed successfully'