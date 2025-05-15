

from app.services.patron_service import create_patron
from flask import request, jsonify

@app.route('/patron', methods=['POST'])
def create_patron_endpoint():
    p_first_name = request.json['first_name']
    p_last_name = request.json['last_name']
    p_email = request.json['email']
    p_phone = request.json['phone']
    p_birth_date = request.json['birth_date']
    create_patron(p_first_name, p_last_name, p_email, p_phone, p_birth_date)
    return jsonify({'message': 'Patron created successfully'})