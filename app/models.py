

from sqlalchemy import Column, Integer, String, Numeric, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func
from sqlalchemy.event import listens_for
from sqlalchemy.types import TypeDecorator, TEXT
import re

Base = declarative_base()

class EmailType(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, email, dialect):
        if email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValueError('Invalid email address')

    def process_result_value(self, value, dialect):
        return value

class Program(Base):
    __tablename__ = 'library_programs'
    program_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    min_participants = Column(Integer, nullable=False)
    cost = Column(Numeric(precision=10, scale=2), nullable=False)
    session_schedule = Column(JSONB, nullable=False)
    registrations = relationship("Registration", backref="program")
    patrons = relationship("Patron", secondary="program_registrations", backref="programs")

class Registration(Base):
    __tablename__ = 'program_registrations'
    registration_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('library_programs.program_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    payment_status = Column(String, nullable=False)
    attendance_log = Column(JSONB, nullable=False)
    patron = relationship("Patron", backref="registrations")

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    email = Column(EmailType, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)