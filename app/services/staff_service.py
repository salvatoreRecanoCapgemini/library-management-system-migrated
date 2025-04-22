

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Staff
import os

def update_staff_status(staff_id, new_status):
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    dbname = os.environ.get('DB_NAME')

    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{dbname}')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        query = session.query(Staff).filter(Staff.staff_id == staff_id).update({Staff.status: new_status}, synchronize_session=False)
        session.execute(query)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()