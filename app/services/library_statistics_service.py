

import datetime
import logging
from typing import Dict, List

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    book_id = Column(Integer)
    loan_date = Column(DateTime)
    due_date = Column(DateTime)
    return_date = Column(DateTime)

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    fine_date = Column(DateTime)
    amount = Column(Float)
    paid = Column(Boolean)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Float)
    copies = Column(Integer)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    event_date = Column(DateTime)
    max_participants = Column(Integer)
    participants = Column(Integer)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(String)

class LibraryStatistics(Base):
    __tablename__ = 'library_statistics'
    id = Column(Integer, primary_key=True)
    total_loans = Column(Integer)
    overdue_loans = Column(Integer)
    active_borrowers = Column(Integer)
    total_fines = Column(Integer)
    paid_fines = Column(Integer)
    pending_fines = Column(Integer)
    books_in_circulation = Column(Integer)
    total_available_copies = Column(Integer)
    average_rating = Column(Float)
    total_events = Column(Integer)
    total_participants = Column(Integer)
    average_capacity_utilization = Column(Float)

def get_loans(p_year: int, p_month: int) -> List[Dict]:
    loans = session.query(Loan).filter(Loan.loan_date >= datetime.date(p_year, p_month, 1),
                                       Loan.loan_date < datetime.date(p_year, p_month + 1, 1)).all()
    return [loan.__dict__ for loan in loans]

def get_fines(p_year: int, p_month: int) -> List[Dict]:
    fines = session.query(Fine).filter(Fine.fine_date >= datetime.date(p_year, p_month, 1),
                                       Fine.fine_date < datetime.date(p_year, p_month + 1, 1)).all()
    return [fine.__dict__ for fine in fines]

def get_books(p_year: int, p_month: int) -> List[Dict]:
    books = session.query(Book).filter(Book.id.in_(session.query(Loan.book_id).filter(Loan.loan_date >= datetime.date(p_year, p_month, 1),
                                                                                       Loan.loan_date < datetime.date(p_year, p_month + 1, 1)))).all()
    return [book.__dict__ for book in books]

def get_events(p_year: int, p_month: int) -> List[Dict]:
    events = session.query(Event).filter(Event.event_date >= datetime.date(p_year, p_month, 1),
                                         Event.event_date < datetime.date(p_year, p_month + 1, 1)).all()
    return [event.__dict__ for event in events]

def insert_into_audit_log(table_name: str, record_id: int, action_type: str, action_timestamp: datetime, new_values: str):
    audit_log = AuditLog(table_name=table_name, record_id=record_id, action_type=action_type, action_timestamp=action_timestamp, new_values=new_values)
    session.add(audit_log)
    session.commit()

def generate_monthly_statistics(p_year: int, p_month: int):
    loans = get_loans(p_year, p_month)
    fines = get_fines(p_year, p_month)
    books = get_books(p_year, p_month)
    events = get_events(p_year, p_month)

    total_loans = len(loans)
    overdue_loans = sum(1 for loan in loans if loan['due_date'] < datetime.date.today())
    active_borrowers = len(set(loan['patron_id'] for loan in loans))

    total_fines = len(fines)
    paid_fines = sum(1 for fine in fines if fine['paid'])
    pending_fines = sum(1 for fine in fines if not fine['paid'])

    books_in_circulation = len(books)
    total_available_copies = sum(book['copies'] for book in books)
    average_rating = sum(book['rating'] for book in books if book['rating']) / len([book for book in books if book['rating']])

    total_events = len(events)
    total_participants = sum(event['participants'] for event in events)
    average_capacity_utilization = sum(event['participants'] / event['max_participants'] for event in events if event['max_participants']) / len([event for event in events if event['max_participants']])

    library_statistics = LibraryStatistics(total_loans=total_loans, overdue_loans=overdue_loans, active_borrowers=active_borrowers,
                                           total_fines=total_fines, paid_fines=paid_fines, pending_fines=pending_fines,
                                           books_in_circulation=books_in_circulation, total_available_copies=total_available_copies,
                                           average_rating=average_rating, total_events=total_events, total_participants=total_participants,
                                           average_capacity_utilization=average_capacity_utilization)
    session.add(library_statistics)
    session.commit()

    insert_into_audit_log('library_statistics', library_statistics.id, 'monthly_report', datetime.datetime.now(), 
                          f'total_loans={total_loans}, overdue_loans={overdue_loans}, active_borrowers={active_borrowers}, '
                          f'total_fines={total_fines}, paid_fines={paid_fines}, pending_fines={pending_fines}, '
                          f'books_in_circulation={books_in_circulation}, total_available_copies={total_available_copies}, '
                          f'average_rating={average_rating}, total_events={total_events}, total_participants={total_participants}, '
                          f'average_capacity_utilization={average_capacity_utilization}')