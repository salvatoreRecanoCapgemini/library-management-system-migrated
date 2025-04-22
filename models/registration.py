

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Registration(Base):
    __tablename__ = 'registrations'

    registration_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.program_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    payment_status = Column(Enum('PAID', 'UNPAID'))
    attendance_log = Column(String)

    program = relationship('Program', backref='registrations')
    patron = relationship('Patron', backref='registrations')