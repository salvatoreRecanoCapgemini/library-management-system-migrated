

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

engine = create_engine('sqlite:///patron.db')
Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    active_loans = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class PatronRepository:
    def get_patron_status(self, patron_id):
        try:
            patron = session.query(Patron).filter_by(id=patron_id).first()
            if patron is None:
                raise ValueError("Patron not found")
            return patron.status, patron.active_loans
        except Exception as e:
            logging.error(f"Error retrieving patron status: {e}")
            raise

    def update_patron_status(self, patron_id, status):
        try:
            if status not in ["active", "inactive"]:
                raise ValueError("Invalid status")
            patron = session.query(Patron).filter_by(id=patron_id).first()
            if patron is None:
                raise ValueError("Patron not found")
            patron.status = status
            session.commit()
        except Exception as e:
            logging.error(f"Error updating patron status: {e}")
            session.rollback()
            raise