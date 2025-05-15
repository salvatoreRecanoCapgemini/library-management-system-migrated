

from app import db

class Membership(db.Model):
    membership_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patron.patron_id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plan.plan_id'))
    end_date = db.Column(db.Date)
    auto_renewal = db.Column(db.Boolean)
    status = db.Column(db.String)