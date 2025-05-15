

from app import db
from app.models.patron import Patron
from app.models.membership_plan import MembershipPlan

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plan.id'))
    end_date = db.Column(db.Date)
    auto_renewal = db.Column(db.Boolean)
    status = db.Column(db.String)

    def __init__(self, patron_id, plan_id, end_date, auto_renewal, status):
        self.patron_id = patron_id
        self.plan_id = plan_id
        self.end_date = end_date
        self.auto_renewal = auto_renewal
        self.status = status

    def has_pending_fines(self):
        patron = Patron.query.get(self.patron_id)
        if patron is None:
            return False
        return patron.fines.any(Fine.status == 'PENDING')

    def has_overdue_items(self):
        patron = Patron.query.get(self.patron_id)
        if patron is None:
            return False
        return patron.loans.any(Loan.status == 'OVERDUE')