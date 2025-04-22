

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from logging import error
from werkzeug.security import generate_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    details = Column(String)

class UserRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_user_data(self, user_id):
        try:
            session = self.Session()
            if not user_id:
                raise ValueError('Invalid user ID')
            user_data = session.query(User).filter_by(id=user_id).first()
            session.close()
            return user_data
        except SQLAlchemyError as e:
            error(e)
            return None

    def create_user(self, user_data):
        try:
            session = self.Session()
            if not user_data.name or not user_data.email or not user_data.password:
                raise ValueError('Invalid user data')
            new_user = User(name=user_data.name, email=user_data.email, password=generate_password_hash(user_data.password))
            session.add(new_user)
            session.commit()
            session.close()
            return True
        except IntegrityError as e:
            session.rollback()
            error(e)
            session.close()
            return False
        except Exception as e:
            session.rollback()
            error(e)
            session.close()
            return False

    def update_user_details(self, user_id, new_details):
        try:
            session = self.Session()
            if not user_id or not new_details:
                raise ValueError('Invalid user ID or details')
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user.details = new_details
                session.commit()
                session.close()
                return user
            else:
                raise ValueError('User not found')
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user_by_email(self, email):
        try:
            session = self.Session()
            if not email:
                raise ValueError('Invalid email')
            user = session.query(User).filter_by(email=email).first()
            session.close()
            return user
        except Exception as e:
            error(e)
            session.close()
            return None

    def update_user_password(self, email, new_password):
        try:
            session = self.Session()
            if not email or not new_password:
                raise ValueError('Invalid email or password')
            user = session.query(User).filter_by(email=email).first()
            if user:
                hashed_password = generate_password_hash(new_password)
                user.password = hashed_password
                session.commit()
                session.close()
                return True
            else:
                raise ValueError('User not found')
        except Exception as e:
            error(e)
            session.close()
            return False