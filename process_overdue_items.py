

from datetime import date, datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    loan_id = Column(Integer)
    amount = Column(Float)
    issue_date = Column(DateTime)
    due_date = Column(DateTime)
    status = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(String)

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    book_id = Column(Integer)
    due_date = Column(DateTime)
    status = Column(String)

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    email = Column(String)

def calculate_fine_amount(due_date):
    return 10.0

def prepare_notification_message(patron_id, book_id, fine_amount):
    return f"Fine of ${fine_amount} for book {book_id} is due for patron {patron_id}"

def process_overdue_items():
    session = Session()
    try:
        # Query database for active loans with due dates earlier than today and no fine issued today
        query = text('SELECT * FROM loans WHERE due_date < :today AND status = \'ACTIVE\' AND NOT EXISTS (SELECT 1 FROM fines WHERE fines.loan_id = loans.loan_id AND fines.issue_date = :today)')
        result = session.execute(query, today=date.today())

        # For each overdue loan, calculate fine amount, create a new fine record, update loan status, prepare a notification message, and create a new audit log record
        for row in result:
            # Calculate fine amount
            fine_amount = calculate_fine_amount(row.due_date)

            # Create a new fine record
            fine = Fine(patron_id=row.patron_id, loan_id=row.loan_id, amount=fine_amount, issue_date=datetime.now(), due_date=datetime.now(), status='ISSUED')
            session.add(fine)

            # Update loan status
            session.execute(text('UPDATE loans SET status = \'OVERDUE\' WHERE loan_id = :loan_id'), loan_id=row.loan_id)

            # Prepare a notification message
            notification_message = prepare_notification_message(row.patron_id, row.book_id, fine_amount)

            # Create a new audit log record
            audit_log = AuditLog(table_name='loans', record_id=row.loan_id, action_type='UPDATE', action_timestamp=datetime.now(), new_values={'status': 'OVERDUE'})
            session.add(audit_log)

        # Commit changes to database, rolling back if an integrity error occurs
        session.commit()

        # Create a temporary table 'notifications' to store notification records
        session.execute(text('CREATE TEMPORARY TABLE notifications (patron_id INTEGER, email VARCHAR(255), message TEXT)'))

        # Process notifications by logging them in the audit_log table
        query = text('SELECT * FROM patrons WHERE id IN (SELECT patron_id FROM loans WHERE due_date < :today AND status = \'OVERDUE\')')
        patrons = session.execute(query, today=date.today())
        for patron in patrons:
            notification = {'patron_id': patron.id, 'email': patron.email, 'message': prepare_notification_message(patron.id, row.book_id, fine_amount)}
            session.execute(text('INSERT INTO notifications (patron_id, email, message) VALUES (:patron_id, :email, :message)'), notification)
            audit_log = AuditLog(table_name='notifications', record_id=notification['patron_id'], action_type='INSERT', action_timestamp=datetime.now(), new_values={'email': notification['email'], 'message': notification['message']})
            session.add(audit_log)

        # Commit changes to database, rolling back if an integrity error occurs
        session.commit()

    except IntegrityError:
        session.rollback()

    finally:
        # Drop temporary table 'notifications'
        session.execute(text('DROP TABLE notifications'))
        session.close()

if __name__ == '__main__':
    process_overdue_items()