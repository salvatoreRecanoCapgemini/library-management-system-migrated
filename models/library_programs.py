

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LibraryPrograms(Base):
    __tablename__ = 'library_programs'
    program_id = Column(Integer, primary_key=True)
    program_name = Column(String)
    program_status = Column(String)
    program_start_date = Column(Date)
    program_end_date = Column(Date)