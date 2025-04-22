

from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User
import logging

log = logging.getLogger(__name__)

def create_user(user_data):
    try:
        if not user_data.name or not user_data.email or not user_data.password:
            raise ValueError('Invalid user data')
        new_user = User(name=user_data.name, email=user_data.email, password=user_data.password)
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        log.error(e)
        return False