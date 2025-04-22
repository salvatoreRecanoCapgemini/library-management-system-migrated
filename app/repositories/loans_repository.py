

from datetime import date
from app import db
from app.models import Loans, Fines

class LoansRepository:
    def get_loan(self, loan_id):
        loan = db.session.query(Loans).filter_by(id=loan_id).first()
        return loan

    def update_loan_status(self, loan_id, status):
        loan = db.session.query(Loans).filter_by(id=loan_id).first()
        loan.status = status
        if status == 'RETURNED':
            loan.return_date = date.today()
        db.session.commit()

    def create_fine_record(self, patron_id, loan_id, amount, issue_date, due_date):
        fine = Fines(patron_id, loan_id, amount, issue_date, due_date)
        db.session.add(fine)
        db.session.commit()