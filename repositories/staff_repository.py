

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from staff_model import Staff
import logging

def update_staff_status(staff_id, new_status):
    if not isinstance(staff_id, int) or not isinstance(new_status, str):
        raise ValueError("Invalid input type")

    engine = create_engine('postgresql://username:password@host:port/dbname')
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        query = session.query(Staff).filter(Staff.staff_id == staff_id).update({Staff.status: new_status})
        session.execute(query)
        session.commit()
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        session.rollback()
        raise e
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        raise e
    finally:
        try:
            session.close()
        except SQLAlchemyError as e:
            logging.error(f"Error closing session: {e}")
        except Exception as e:
            logging.error(f"Unknown error: {e}")