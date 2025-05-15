

from app.models.fine import Fine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import Error

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()

class FineRepository:
    def retrieve_fine(self, fine_id, status):
        try:
            if not isinstance(fine_id, int) or not isinstance(status, str):
                raise ValueError("Invalid input type")
            fine = session.query(Fine).filter_by(fine_id=fine_id, status=status).first()
            if fine is None:
                raise ValueError("Fine not found")
            return fine
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        except Error as e:
            raise e

    def update_fine(self, fine):
        try:
            if not isinstance(fine, Fine):
                raise ValueError("Invalid input type")
            session.query(Fine).filter_by(fine_id=fine.fine_id).update({"status": fine.status, "payment_date": fine.payment_date})
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        except Error as e:
            raise e