

from sqlalchemy import create_engine, Column, Integer, String, Date, Decimal, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta, date

Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    due_date = Column(Date)
    status = Column(String)
    extensions_count = Column(Integer, default=0)
    patron = relationship("Patron", backref="loans")
    book = relationship("Book", backref="loans")

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    amount = Column(Decimal)
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_log'
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
    author = Column(String)
    availability = Column(Integer)

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    status = Column(String)

class LoanRepository:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_book_loan(self, patron_id, book_id, loan_days):
        available_copies = self.get_book_availability(book_id)
        if available_copies <= 0:
            raise Exception("Book is not available for loan")

        patron_status, active_loans = self.get_patron_status(patron_id)
        if patron_status != 'ACTIVE':
            raise Exception("Patron account is not active")
        if active_loans >= 5:
            raise Exception("Patron has reached maximum number of loans")

        loan_id = self.create_loan_record(patron_id, book_id, loan_days)
        self.set_loan_status(loan_id, 'ACTIVE')

        self.update_book_availability(book_id, -1)

    def get_active_loans(self):
        try:
            active_loans = self.session.query(Loan).filter(Loan.due_date < date.today(), Loan.status == 'ACTIVE').all()
            return active_loans
        except Exception as e:
            print(e)
            return None

    def update_loan_status(self, loan_id):
        try:
            loan = self.session.query(Loan).filter_by(loan_id=loan_id).first()
            loan.status = 'OVERDUE'
            self.session.commit()
        except Exception as e:
            print(e)

    def process_overdue_loans(self):
        overdue_loans = self.session.query(Loan).filter(Loan.due_date < date.today(), Loan.status == 'ACTIVE').all()

        for loan in overdue_loans:
            fine_amount = self.calculate_fine_amount(loan.due_date)

            fine = Fine(patron_id=loan.patron_id, loan_id=loan.loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today(), status='ISSUED')
            self.session.add(fine)

            loan.status = 'OVERDUE'
            self.session.add(loan)

            notification_message = self.prepare_notification_message(loan, fine_amount)

            audit_log = AuditLog(table_name='loans', record_id=loan.loan_id, action_type='NOTIFICATION', action_timestamp=datetime.now(), new_values=notification_message)
            self.session.add(audit_log)

        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()

    def get_loans(self, date_range):
        loans = self.session.query(Loan).filter(Loan.due_date.between(date_range[0], date_range[1])).all()
        return loans

    def extend_loan_period(self, loan_id, extension_days=7):
        loan_details = self.session.query(Loan).filter_by(loan_id=loan_id, status='ACTIVE').first()
        if loan_details is None:
            raise Exception('Active loan not found')
        if loan_details.extensions_count >= 2:
            raise Exception('Maximum extensions reached')

        pending_reservations = self.session.query(Reservations).filter_by(book_id=loan_details.book_id, status='PENDING').first()
        if pending_reservations is not None:
            raise Exception('Book has pending reservations')

        new_due_date = loan_details.due_date + timedelta(days=extension_days)
        new_extensions_count = loan_details.extensions_count + 1

        loan_details.due_date = new_due_date
        loan_details.extensions_count = new_extensions_count
        self.session.commit()

    def process_book_return(self, loan_id):
        loan_details = self.session.query(Loan).filter_by(loan_id=loan_id).first()
        if loan_details is None or loan_details.status != 'ACTIVE':
            raise Exception('Loan does not exist or is not active')

        book_id = loan_details.book_id
        patron_id = loan_details.patron_id
        due_date = loan_details.due_date

        days_overdue = (date.today() - due_date).days
        if days_overdue > 0:
            fine_amount = days_overdue * 0.50
            fine = Fine(patron_id=patron_id, loan_id=loan_id, amount=fine_amount, issue_date=date.today(), due_date=date.today() + timedelta(days=14), status='PENDING')
            self.session.add(fine)
            self.session.commit()

        loan_details.status = 'RETURNED'
        self.session.commit()
        self.update_book_availability(book_id, 1)

    def get_book_availability(self, book_id):
        book = self.session.query(Book).filter_by(book_id=book_id).first()
        return book.availability

    def get_patron_status(self, patron_id):
        patron = self.session.query(Patron).filter_by(patron_id=patron_id).first()
        active_loans = len(self.session.query(Loan).filter_by(patron_id=patron_id, status='ACTIVE').all())
        return patron.status, active_loans

    def create_loan_record(self, patron_id, book_id, loan_days):
        loan = Loan(patron_id=patron_id, book_id=book_id, due_date=date.today() + timedelta(days=loan_days), status='ACTIVE')
        self.session.add(loan)
        self.session.commit()
        return loan.loan_id

    def set_loan_status(self, loan_id, status):
        loan = self.session.query(Loan).filter_by(loan_id=loan_id).first()
        loan.status = status
        self.session.commit()

    def update_book_availability(self, book_id, availability):
        book = self.session.query(Book).filter_by(book_id=book_id).first()
        book.availability += availability
        self.session.commit()

    def calculate_fine_amount(self, due_date):
        days_overdue = (date.today() - due_date).days
        return days_overdue * 0.50

    def prepare_notification_message(self, loan, fine_amount):
        patron_name = loan.patron.name
        book_title = loan.book.title
        return f"Notification for patron {patron_name} for book {book_title} with fine amount {fine_amount}"