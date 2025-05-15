

from datetime import date, timedelta, datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///library.db')
Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    book_id = Column(Integer)
    due_date = Column(Date)
    status = Column(String)
    extensions_count = Column(Integer)

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    loan_id = Column(Integer)
    amount = Column(Float)
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    log_id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(String)

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    availability = Column(Integer)

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    first_name = Column(String)

class Reservations(Base):
    __tablename__ = 'reservations'
    reservation_id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    patron_id = Column(Integer)
    status = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db = Session()

def process_overdue_loans():
    loans = db.query(Loan).filter(Loan.due_date < date.today(), Loan.status == 'ACTIVE').all()
    for loan in loans:
        fine_amount = calculate_fine_amount(loan)
        fine = Fine(patron_id=loan.patron_id, loan_id=loan.loan_id, amount=fine_amount, issue_date=date.today())
        db.add(fine)
        loan.status = 'OVERDUE'
        db.add(loan)
        notification_text = prepare_notification_text(loan, fine_amount)
        audit_log = AuditLog(table_name='loans', record_id=loan.loan_id, action_type='NOTIFICATION', action_timestamp=datetime.now(), new_values=notification_text)
        db.add(audit_log)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

def calculate_fine_amount(loan):
    fine_amount = (date.today() - loan.due_date).days * 0.5
    return fine_amount

def prepare_notification_text(loan, fine_amount):
    patron = db.query(Patron).get(loan.patron_id)
    book = db.query(Book).get(loan.book_id)
    notification_text = f'Dear {patron.first_name}, your book {book.title} is overdue. Please pay a fine of {fine_amount}. '
    return notification_text

def extend_loan_period(p_loan_id, p_extension_days=7):
    loan_details = db.query(Loan).filter_by(loan_id=p_loan_id, status='ACTIVE').first()
    if loan_details is None:
        raise Exception('Active loan not found')
    if loan_details.extensions_count >= 2:
        raise Exception('Maximum extensions reached')
    pending_reservations = db.query(Reservations).filter_by(book_id=loan_details.book_id, status='PENDING').first()
    if pending_reservations is not None:
        raise Exception('Book has pending reservations')
    new_due_date = loan_details.due_date + timedelta(days=p_extension_days)
    new_extensions_count = loan_details.extensions_count + 1
    loan_details.due_date = new_due_date
    loan_details.extensions_count = new_extensions_count
    db.commit()

def process_book_return(p_loan_id):
    loan_details = db.query(Loan).get(p_loan_id)
    if loan_details is None or loan_details.status != 'ACTIVE':
        raise Exception('Loan does not exist or is not active')
    book_id = loan_details.book_id
    patron_id = loan_details.patron_id
    due_date = loan_details.due_date
    days_overdue = (date.today() - due_date).days
    if days_overdue > 0:
        fine_amount = days_overdue * 0.5
        fine = Fine(patron_id=patron_id, loan_id=p_loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today() + timedelta(days=14), status='PENDING')
        db.add(fine)
        db.commit()
    loan_details.status = 'RETURNED'
    db.commit()
    update_book_availability(book_id, 1)

def update_book_availability(book_id, increment):
    book = db.query(Book).get(book_id)
    book.availability += increment
    db.commit()