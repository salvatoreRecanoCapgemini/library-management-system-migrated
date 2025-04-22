

from sqlalchemy import update, create_engine
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.orm import sessionmaker
import logging

def update_staff_status(staff_id, new_status):
    engine = create_engine('postgresql://username:password@host:port/database')
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        if not session.query(Staff).filter(Staff.staff_id == staff_id).first():
            raise ValueError("Staff ID does not exist")
        if new_status not in ["active", "inactive"]:
            raise ValueError("Invalid new status value")
        update_stmt = update(Staff).where(Staff.staff_id == staff_id).values(status=new_status)
        session.execute(update_stmt)
        session.commit()
        logging.info(f"Updated staff status for staff ID {staff_id} to {new_status}")
    except IntegrityError as e:
        session.rollback()
        logging.error(f"Integrity error: {e}")
        raise e
    except DatabaseError as e:
        session.rollback()
        logging.error(f"Database error: {e}")
        raise e
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        raise e
    finally:
        session.close()