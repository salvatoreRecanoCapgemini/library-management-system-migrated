

from datetime import date
from decimal import Decimal
from sqlalchemy import exc
from app.models import Fine
from app import db
import logging

class FineService:
    def process_fine_payment(self, fine_id: int, paid_amount: Decimal):
        try:
            if not isinstance(fine_id, int) or fine_id <= 0:
                raise ValueError('Invalid fine_id')
            if paid_amount <= Decimal('0.00'):
                raise ValueError('Paid amount must be a positive value')
            fine = Fine.query.filter_by(id=fine_id, status='PENDING').first()
            if fine is None:
                raise exc.NoResultFound('Valid unpaid fine not found')
            remaining_amount = fine.amount - paid_amount
            if remaining_amount > Decimal('0.00'):
                raise ValueError('Partial payments not supported')
            fine.status = 'PAID'
            fine.payment_date = date.today()
            fine.process_payment(paid_amount)
            db.session.commit()
        except exc.NoResultFound as e:
            logging.error(f'Error processing fine payment: {e}')
            raise
        except ValueError as e:
            logging.error(f'Error processing fine payment: {e}')
            raise
        except Exception as e:
            logging.error(f'Error processing fine payment: {e}')
            db.session.rollback()
            raise