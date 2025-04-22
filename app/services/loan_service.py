

from datetime import date, timedelta, datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///loan_service.db')
Base = declarative_base()
metadata = MetaData()

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    email = Column(String)

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    available_copies = Column(Integer)

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    loan_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date)
    status = Column(String)
    extensions_count = Column(Integer)

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    amount = Column(Float)
    issue_date = Column(Date)
    due_date = Column(Date)

class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    email = Column(String)
    message = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    audit_log_id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(String)

class Reservation(Base):
    __tablename__ = 'reservations'
    reservation_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'))
    status = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class LoanService:
    def process_book_loan(self, patron_id, book_id, loan_days):
        patron = session.query(Patron).get(patron_id)
        book = session.query(Book).get(book_id)
        if patron and book:
            loan = Loan(patron_id=patron_id, book_id=book_id, loan_date=date.today(), due_date=date.today() + timedelta(days=loan_days), status='ACTIVE', extensions_count=0)
            session.add(loan)
            session.commit()

    def extend_loan_period(self, loan_id, extension_days=14):
        loan = session.query(Loan).get(loan_id)
        if loan.status != 'ACTIVE':
            raise ValueError('Active loan not found')
        if loan.extensions_count >= 2:
            raise ValueError('Maximum extensions reached')
        reservation = session.query(Reservation).filter_by(book_id=loan.book_id, status='PENDING').first()
        if reservation:
            raise ValueError('Book has pending reservations')
        loan.due_date = loan.due_date + timedelta(days=extension_days)
        loan.extensions_count = loan.extensions_count + 1
        session.commit()

    def process_book_return(self, loan_id):
        loan = session.query(Loan).get(loan_id)
        if loan is None or loan.status != 'ACTIVE':
            raise Exception('Loan not found or not active')
        overdue_days = (date.today() - loan.due_date).days
        if overdue_days > 0:
            fine_amount = overdue_days * 0.50
            fine = Fine(patron_id=loan.patron_id, loan_id=loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today() + timedelta(days=30))
            session.add(fine)
        loan.status = 'RETURNED'
        loan.return_date = date.today()
        session.commit()
        book = session.query(Book).get(loan.book_id)
        book.available_copies += 1
        session.commit()

    def process_overdue_loans(self):
        overdue_loans = session.query(Loan).filter(Loan.due_date < date.today(), Loan.status == 'ACTIVE').all()
        for loan in overdue_loans:
            fine_amount = (date.today() - loan.due_date).days * 0.50
            fine = Fine(patron_id=loan.patron_id, loan_id=loan.loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today() + timedelta(days=14))
            session.add(fine)
            loan.status = 'OVERDUE'
            session.commit()
            notification = Notification(patron_id=loan.patron_id, email=loan.patron.email, message=f'Overdue book: {loan.book.title}. Fine amount: {fine_amount}')
            session.add(notification)
            audit_log = AuditLog(table_name='notifications', record_id=notification.notification_id, action_type='INSERT', action_timestamp=datetime.now(), new_values={'notification_id': notification.notification_id, 'patron_id': notification.patron_id, 'email': notification.email, 'message': notification.message})
            session.add(audit_log)
        notifications_table = Table('notifications', metadata, autoload=True)
        for notification in session.query(notifications_table).all():
            audit_log = AuditLog(table_name='audit_log', record_id=notification.notification_id, action_type='INSERT', action_timestamp=datetime.now(), new_values={'notification_id': notification.notification_id, 'patron_id': notification.patron_id, 'email': notification.email, 'message': notification.message})
            session.add(audit_log)
        session.commit()
        metadata.drop_all(tables=[notifications_table])