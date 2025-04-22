

from flask import request, jsonify
from app.services.patron_service import PatronService

class PatronController:
    def __init__(self, patron_service):
        self.patron_service = patron_service

    def create_patron(self):
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        birth_date = data['birth_date']
        self.patron_service.create_patron(first_name, last_name, email, phone, birth_date)
        return jsonify({'message': 'Patron created successfully'})