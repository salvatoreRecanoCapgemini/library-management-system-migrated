

from app.models.fine import Fine
from app.repositories.fine_repository import FineRepository
from sqlalchemy.exc import IntegrityError
from datetime import date
from app import db

class FineService:
    def __init__(self):
        self.fine_repository = FineRepository()

    def process_fine_payment(self, p_fine_id, p_amount_paid):
        fine = self.fine_repository.retrieve_fine(p_fine_id, 'PENDING')
        if fine is None:
            raise Exception('Valid unpaid fine not found')
        total_amount = fine.amount
        if p_amount_paid < total_amount:
            raise Exception('Partial payments not supported')
        fine.status = 'PAID'
        fine.payment_date = date.today()
        try:
            self.fine_repository.update_fine(fine)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e