

from datetime import date, datetime
import calendar
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()
metadata = MetaData()

class Loans(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    loan_date = Column(DateTime)
    due_date = Column(DateTime)
    patron_id = Column(Integer)

class Fines(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    fine_date = Column(DateTime)
    payment_status = Column(String)

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    publication_date = Column(DateTime)
    rating = Column(Integer)

class LibraryEvents(Base):
    __tablename__ = 'library_events'
    id = Column(Integer, primary_key=True)
    event_date = Column(DateTime)
    participant_count = Column(Integer)
    max_participants = Column(Integer)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(JSON)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db = Session()

class StatisticsService:
    def generate_monthly_statistics(self, p_year, p_month):
        try:
            v_start_date = date(p_year, p_month, 1)
            v_end_date = date(p_year, p_month, calendar.monthrange(p_year, p_month)[1])

            total_loans = 0
            overdue_loans = 0
            active_borrowers = set()
            total_fines = 0
            paid_fines = 0
            pending_fines = 0
            books_in_circulation = 0
            total_available_copies = 0
            average_rating = 0
            total_events = 0
            total_participants = 0
            average_capacity_utilization = 0

            loans = db.query(Loans).filter(Loans.loan_date >= v_start_date, Loans.loan_date <= v_end_date).all()
            for loan in loans:
                total_loans += 1
                if loan.due_date < date.today():
                    overdue_loans += 1
                active_borrowers.add(loan.patron_id)

            fines = db.query(Fines).filter(Fines.fine_date >= v_start_date, Fines.fine_date <= v_end_date).all()
            for fine in fines:
                total_fines += 1
                if fine.payment_status == 'paid':
                    paid_fines += 1
                elif fine.payment_status == 'pending':
                    pending_fines += 1

            books = db.query(Books).filter(Books.publication_date >= v_start_date, Books.publication_date <= v_end_date).all()
            for book in books:
                books_in_circulation += 1
                total_available_copies += 1
                if book.rating:
                    average_rating += book.rating

            events = db.query(LibraryEvents).filter(LibraryEvents.event_date >= v_start_date, LibraryEvents.event_date <= v_end_date).all()
            for event in events:
                total_events += 1
                total_participants += event.participant_count
                if event.max_participants:
                    average_capacity_utilization += event.participant_count / event.max_participants

            v_result = {
                'total_loans': total_loans,
                'overdue_loans': overdue_loans,
                'active_borrowers': len(active_borrowers),
                'total_fines': total_fines,
                'paid_fines': paid_fines,
                'pending_fines': pending_fines,
                'books_in_circulation': books_in_circulation,
                'total_available_copies': total_available_copies,
                'average_rating': average_rating / books_in_circulation if books_in_circulation > 0 else 0,
                'total_events': total_events,
                'total_participants': total_participants,
                'average_capacity_utilization': average_capacity_utilization / total_events if total_events > 0 else 0
            }

            v_stats = json.dumps(v_result)

            db.add(AuditLog(table_name='statistics', record_id=None, action_type='insert', action_timestamp=datetime.now(), new_values=v_stats))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e