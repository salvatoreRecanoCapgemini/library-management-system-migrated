

from sqlalchemy import create_engine, Column, Integer, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import text
import enum

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    status = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class StaffStatus(enum.Enum):
    active = 'active'
    inactive = 'inactive'

class StaffService:
    def update_staff_status(self, staff_id, new_status):
        if not isinstance(new_status, str) or new_status not in [status.value for status in StaffStatus]:
            raise ValueError("Invalid new_status")

        try:
            staff = session.query(Staff).get(staff_id)
            if staff is None:
                raise ValueError("Invalid staff_id")

            update_staff_status_sql = text('''
                UPDATE staff
                SET status = :new_status
                WHERE id = :staff_id
            ''')
            session.execute(update_staff_status_sql, {'new_status': new_status, 'staff_id': staff_id})
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError("Invalid new_status")
        finally:
            session.close()