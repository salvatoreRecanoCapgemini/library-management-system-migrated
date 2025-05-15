

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Staff(Base):
    __tablename__ = 'staff'
    staff_id = Column(Integer, primary_key=True)
    status = Column(String)