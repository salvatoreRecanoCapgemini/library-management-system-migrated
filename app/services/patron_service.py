

from app.models.patron import Patron
from app import db
from datetime import date

def create_patron(p_first_name, p_last_name, p_email, p_phone, p_birth_date):
    try:
        if not p_first_name or not p_last_name or not p_email or not p_phone or not p_birth_date:
            raise ValueError("All parameters are required")

        patron = Patron(first_name=p_first_name, last_name=p_last_name, email=p_email, phone=p_phone, membership_date=date.today(), status='ACTIVE', birth_date=p_birth_date)
        db.session.add(patron)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e