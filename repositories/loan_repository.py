

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float
from datetime import date

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    book_id = Column(Integer)
    loan_days = Column(Integer)
    due_date = Column(Date)
    status = Column(String)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    available_copies = Column(Integer)

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    loan_id = Column(Integer)
    fine_amount = Column(Float)
    due_date = Column(Date)
    status = Column(String)

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    status = Column(String)

Base.metadata.create_all(engine)

class LoanRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_loans(self):
        loan_data = self.db_session.query(Loan).all()
        return loan_data

    def create_loan_record(self, patron_id, book_id, loan_days):
        loan = Loan(patron_id=patron_id, book_id=book_id, loan_days=loan_days)
        self.db_session.add(loan)
        self.db_session.commit()

    def update_loan_status(self, loan_id, status):
        loan = self.db_session.query(Loan).filter_by(id=loan_id).first()
        if loan is None:
            raise ValueError("Loan not found")
        loan.status = status
        self.db_session.commit()

    def process_book_loan(self, patron_id, book_id, loan_days):
        available_copies = self.get_available_copies(book_id)
        if available_copies <= 0:
            raise ValueError("Book is not available for loan")
        patron_status, active_loans = self.get_patron_status_and_active_loans(patron_id)
        if patron_status != "ACTIVE" or active_loans >= 5:
            raise ValueError("Patron's account is not active or they have reached the maximum number of loans")
        self.create_loan_record(patron_id, book_id, loan_days)
        self.update_book_availability(book_id, -1)

    def retrieve_loan_details(self, loan_id):
        loan_details = self.db_session.query(Loan).filter_by(id=loan_id).first()
        if loan_details is None:
            raise ValueError("Loan not found")
        return loan_details

    def calculate_days_overdue(self, due_date):
        current_date = date.today()
        days_overdue = (current_date - due_date).days
        return days_overdue

    def calculate_fine_amount(self, days_overdue):
        fine_amount = days_overdue * 0.50
        return fine_amount

    def create_fine_object(self, patron_id, loan_id, fine_amount, due_date):
        fine = Fine(patron_id, loan_id, fine_amount, due_date, 'ACTIVE')
        return fine

    def insert_fine(self, fine):
        try:
            self.db_session.add(fine)
            self.db_session.commit()
        except Exception as e:
            raise Exception("Failed to insert fine: " + str(e))

    def update_book_availability(self, book_id, increment):
        book = self.db_session.query(Book).filter_by(id=book_id).first()
        if book is None:
            raise ValueError("Book not found")
        book.available_copies += increment
        self.db_session.commit()

    def process_book_return(self, loan_id):
        loan_details = self.retrieve_loan_details(loan_id)
        if loan_details.status != 'ACTIVE':
            raise Exception('Active loan not found')
        book_id = loan_details.book_id
        patron_id = loan_details.patron_id
        due_date = loan_details.due_date
        days_overdue = self.calculate_days_overdue(due_date)
        if days_overdue > 0:
            fine_amount = self.calculate_fine_amount(days_overdue)
            fine = self.create_fine_object(patron_id, loan_id, fine_amount, due_date)
            self.insert_fine(fine)
        self.update_loan_status(loan_id, 'RETURNED')
        self.update_book_availability(book_id, 1)

    def get_available_copies(self, book_id):
        book = self.db_session.query(Book).filter_by(id=book_id).first()
        if book is None:
            raise ValueError("Book not found")
        return book.available_copies

    def get_patron_status_and_active_loans(self, patron_id):
        patron = self.db_session.query(Patron).filter_by(id=patron_id).first()
        if patron is None:
            raise ValueError("Patron not found")
        active_loans = self.db_session.query(Loan).filter_by(patron_id=patron_id, status='ACTIVE').count()
        return patron.status, active_loans