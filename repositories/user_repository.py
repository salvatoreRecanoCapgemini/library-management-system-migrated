

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from logging import error
from werkzeug.security import generate_password_hash
from .models import User, Base

class UserRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_user(self, user_data):
        if user_data is None:
            raise ValueError('User data is None')
        try:
            if not user_data.name or not user_data.email or not user_data.password:
                raise ValueError('Invalid user data')
            existing_user = self.session.query(User).filter_by(email=user_data.email).first()
            if existing_user:
                raise ValueError('User already exists')
            user_data.password = generate_password_hash(user_data.password)
            new_user = User(name=user_data.name, email=user_data.email, password=user_data.password)
            self.session.add(new_user)
            self.session.commit()
            return new_user.id
        except SQLAlchemyError as e:
            self.session.rollback()
            error(e)
            return None

    def get_user_by_id(self, user_id):
        if user_id is None:
            raise ValueError('User ID is None')
        try:
            if not user_id:
                raise ValueError('Invalid user ID')
            user_data = self.session.query(User).filter_by(id=user_id).first()
            if not user_data:
                raise ValueError('User not found')
            return user_data
        except SQLAlchemyError as e:
            error(e)
            return None

    def update_user_details(self, user_id, new_details):
        if new_details is None:
            raise ValueError('New details are None')
        try:
            if not user_id:
                raise ValueError('Invalid user ID')
            user_data = self.session.query(User).filter_by(id=user_id).first()
            if not user_data:
                raise ValueError('User not found')
            if not new_details.name or not new_details.email or not new_details.password:
                raise ValueError('Invalid new details')
            user_data.name = new_details.name
            user_data.email = new_details.email
            user_data.password = generate_password_hash(new_details.password)
            self.session.commit()
            return user_data
        except SQLAlchemyError as e:
            self.session.rollback()
            error(e)
            return None

    @property
    def session(self):
        return self.Session()