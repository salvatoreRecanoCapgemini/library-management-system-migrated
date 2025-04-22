

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.patron import Patron
from datetime import date
import logging

class PatronService:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        logging.basicConfig(level=logging.INFO)

    def create_patron(self, first_name, last_name, email, phone, birth_date):
        try:
            if not first_name or not last_name or not email or not phone or not birth_date:
                logging.error("Invalid input: All fields are required")
                return False
            patron = Patron(first_name=first_name, last_name=last_name, email=email, phone=phone, birth_date=birth_date, membership_date=date.today(), status='ACTIVE')
            self.session.add(patron)
            self.session.commit()
            logging.info("Patron created successfully")
            return True
        except Exception as e:
            logging.error(f"Error creating patron: {str(e)}")
            self.session.rollback()
            return False