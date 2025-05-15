

from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProgramRegistrations(Base):
    __tablename__ = 'program_registrations'
    registration_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('library_programs.program_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    registration_date = Column(Date)