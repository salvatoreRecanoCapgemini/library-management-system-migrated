

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from logging import error
from datetime import date

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    membership_date = Column(Date)
    status = Column(String)
    birth_date = Column(Date)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_user(user_data):
    try:
        if not user_data.name or not user_data.email or not user_data.password:
            raise ValueError('Invalid user data')

        existing_user = session.query(User).filter_by(email=user_data.email).first()
        if existing_user:
            raise ValueError('User already exists')

        user = User(name=user_data.name, email=user_data.email, password=user_data.password)
        session.add(user)
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        error(e)
        return False
    except Exception as e:
        session.rollback()
        error(e)
        return False

def get_user_data(user_id):
    try:
        user_data = session.query(User).filter_by(id=user_id).first()
        return user_data
    except SQLAlchemyError as e:
        error(e)
        return None

def update_user_details(user_id, updated_details):
    try:
        if user_id <= 0:
            raise ValueError('Invalid user ID')

        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.name = updated_details.name
            user.email = updated_details.email
            user.password = updated_details.password
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        error(e)
        return False

def create_patron(p_first_name, p_last_name, p_email, p_phone, p_birth_date):
    try:
        if not p_first_name or not p_last_name or not p_email or not p_phone or not p_birth_date:
            raise ValueError('Invalid patron data')

        existing_patron = session.query(Patron).filter_by(email=p_email).first()
        if existing_patron:
            raise ValueError('Patron already exists')

        new_patron = Patron(
            first_name=p_first_name,
            last_name=p_last_name,
            email=p_email,
            phone=p_phone,
            membership_date=date.today(),
            status='ACTIVE',
            birth_date=p_birth_date
        )
        session.add(new_patron)
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        error(e)
        return False
    except Exception as e:
        session.rollback()
        error(e)
        return False