

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MembershipPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    duration_months = db.Column(db.Integer)

    def __init__(self, price, duration_months):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(duration_months, int) or duration_months <= 0:
            raise ValueError("Duration months must be a positive integer")
        self.price = price
        self.duration_months = duration_months