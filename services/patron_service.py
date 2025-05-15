

from models.patron import Patron
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

def create_patron(p_first_name, p_last_name, p_email, p_phone, p_birth_date):
    if not p_first_name or not p_last_name or not p_email or not p_phone or not p_birth_date:
        logging.error("Invalid input parameters")
        raise ValueError("Invalid input parameters")

    try:
        with Session() as session:
            existing_patron = session.query(Patron).filter_by(email=p_email).first()
            if existing_patron:
                logging.error("Patron with the same email already exists")
                raise ValueError("Patron with the same email already exists")

            existing_patron = session.query(Patron).filter_by(phone=p_phone).first()
            if existing_patron:
                logging.error("Patron with the same phone number already exists")
                raise ValueError("Patron with the same phone number already exists")

            patron = Patron(first_name=p_first_name, last_name=p_last_name, email=p_email, phone=p_phone, birth_date=p_birth_date)
            session.add(patron)
            session.commit()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise