

package app.models

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Staff(Base):
    __tablename__ = 'staff'
    staff_id = Column(Integer, primary_key=True)
    status = Column(String)

    def __init__(self, staff_id, status):
        self.staff_id = staff_id
        self.status = status

    def update_status(self, new_status):
        engine = create_engine('sqlite:///staff.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        staff = session.query(Staff).filter_by(staff_id=self.staff_id).first()
        if staff:
            valid_statuses = ["active", "inactive"]
            if new_status in valid_statuses:
                staff.status = new_status
                session.commit()
            else:
                raise ValueError("Invalid new_status")
        else:
            raise ValueError("Invalid staff_id")