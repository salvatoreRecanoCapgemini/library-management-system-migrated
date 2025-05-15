

package app.controllers

import app.services.PatronService
import logging
from datetime import datetime
from typing import Dict

class PatronController:
    def __init__(self):
        self.patron_service = PatronService()

    def create(self, patron_data: Dict) -> str:
        try:
            first_name = patron_data.get('first_name')
            last_name = patron_data.get('last_name')
            email = patron_data.get('email')
            phone = patron_data.get('phone')
            birth_date = datetime.strptime(patron_data.get('birth_date'), '%Y-%m-%d')

            if not all([first_name, last_name, email, phone, birth_date]):
                raise ValueError('Invalid patron data')

            self.patron_service.create_patron(first_name, last_name, email, phone, birth_date)
            logging.info('Patron created successfully')
            return 'Patron created successfully'
        except ValueError as e:
            logging.error(f'Invalid patron data: {e}')
            return 'Invalid patron data'
        except Exception as e:
            logging.error(f'Error creating patron: {e}')
            return 'Error creating patron'