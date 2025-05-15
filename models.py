

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

class Program(Base):
    __tablename__ = 'program'
    program_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    min_participants = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    session_schedule = Column(JSON, nullable=False)
    registrations = relationship('Registration', backref='program')

class Registration(Base):
    __tablename__ = 'registration'
    registration_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('program.program_id'))
    patron_id = Column(Integer, ForeignKey('patron.patron_id'))
    payment_status = Column(String(50), nullable=False)
    attendance_log = Column(JSON, nullable=False)
    patron = relationship('Patron', backref='registrations')
    program = relationship('Program', backref='registrations')

class Patron(Base):
    __tablename__ = 'patron'
    patron_id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    loans = relationship('Loan', backref='patron')
    fines = relationship('Fine', backref='patron')
    registrations = relationship('Registration', backref='patron')

class Loan(Base):
    __tablename__ = 'loan'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patron.patron_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    due_date = Column(Date)
    status = Column(String)
    book = relationship('Book', backref='loans')
    fine = relationship('Fine', backref='loan')
    patron = relationship('Patron', backref='loans')

class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    loans = relationship('Loan', backref='book')

class Fine(Base):
    __tablename__ = 'fine'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patron.patron_id'))
    loan_id = Column(Integer, ForeignKey('loan.loan_id'))
    amount = Column(Float)
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)
    patron = relationship('Patron', backref='fines')
    loan = relationship('Loan', backref='fine')

class AuditLog(Base):
    __tablename__ = 'audit_log'
    log_id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(String)

Base.metadata.create_all(engine)