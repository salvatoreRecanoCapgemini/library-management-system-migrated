

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MembershipPlan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    duration_months = db.Column(db.Integer)