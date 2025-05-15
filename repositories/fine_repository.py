

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Fine

class FineRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_fine_object(self, patron_id, loan_id, fine_amount, due_date):
        fine = Fine(patron_id, loan_id, fine_amount, due_date)
        return fine

    def insert_fine(self, fine):
        self.db_session.add(fine)

    def get_fine_by_id(self, fine_id):
        fine = self.db_session.query(Fine).filter(Fine.fine_id == fine_id).first()
        return fine

    def update_fine_status(self, fine, status):
        fine.status = status
        self.db_session.add(fine)

    def commit_changes(self):
        try:
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def process_fine_payment(self, p_fine_id, p_amount_paid):
        fine = self.get_fine_by_id(p_fine_id)
        if fine is None:
            raise Exception('Fine not found')
        if fine.status != 'PENDING':
            raise Exception('Fine is not pending')
        total_amount = fine.amount
        if p_amount_paid < total_amount:
            remaining_amount = total_amount - p_amount_paid
            raise Exception('Partial payments not supported')
        self.update_fine_status(fine, 'PAID')
        fine.payment_date = datetime.now()
        self.commit_changes()