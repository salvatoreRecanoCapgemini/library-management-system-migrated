

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import CheckConstraint

Base = declarative_base()

class Patrons(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    patron_name = Column(String(50), nullable=False)
    patron_email = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint('patron_name != ""', name='check_patron_name'),
        CheckConstraint('patron_email != ""', name='check_patron_email'),
        CheckConstraint('email != ""', name='check_email'),
        CheckConstraint('first_name != ""', name='check_first_name'),
    )

    def __init__(self, patron_name, patron_email, email, first_name):
        self.patron_name = patron_name
        self.patron_email = patron_email
        self.email = email
        self.first_name = first_name

    def __repr__(self):
        return f"Patrons(patron_id={self.patron_id}, patron_name='{self.patron_name}', patron_email='{self.patron_email}', email='{self.email}', first_name='{self.first_name}')"

def create_database():
    engine = create_engine('sqlite:///patrons.db')
    Base.metadata.create_all(engine)

def create_session():
    engine = create_engine('sqlite:///patrons.db')
    Session = sessionmaker(bind=engine)
    return Session()

def add_patron(session, patron):
    try:
        session.add(patron)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding patron: {e}")

def get_patron(session, patron):
    try:
        session.query(Patrons).filter(Patrons.patron_id == patron.patron_id).first()
    except SQLAlchemyError as e:
        print(f"Error getting patron: {e}")

def update_patron(session, patron):
    try:
        session.query(Patrons).filter(Patrons.patron_id == patron.patron_id).update({'patron_name': patron.patron_name, 'patron_email': patron.patron_email, 'email': patron.email, 'first_name': patron.first_name})
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating patron: {e}")

def delete_patron(session, patron_id):
    try:
        session.query(Patrons).filter(Patrons.patron_id == patron_id).delete()
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting patron: {e}")