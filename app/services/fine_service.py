

from datetime import date
from app.models import Fine
from app import db

class FineService:
    def process_fine_payment(self, fine_id, amount_paid):
        fine = Fine.query.filter_by(fine_id=fine_id, status='PENDING').first()
        if fine is None:
            raise Exception('Valid unpaid fine not found')
        total_amount = fine.amount
        if amount_paid < total_amount:
            remaining_amount = total_amount - amount_paid
            raise Exception('Partial payments not supported')
        fine.status = 'PAID'
        fine.payment_date = date.today()
        db.session.commit()