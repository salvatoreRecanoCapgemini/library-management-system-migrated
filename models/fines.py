

from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from datetime import date

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    amount = Column(String)
    issue_date = Column(Date)
    due_date = Column(Date)
    status = Column(String)
    fine_amount = Column(Integer)
    paid_amount = Column(Integer)
    payment_date = Column(Date)

    patron = relationship('Patron', backref='fines')
    loan = relationship('Loan', backref='fines')

    def __init__(self, patron_id, loan_id, amount, issue_date, due_date, status, fine_amount, paid_amount, payment_date):
        self.patron_id = self.validate_integer(patron_id)
        loan_id = self.validate_integer(loan_id)
        amount = self.validate_string(amount)
        issue_date = self.validate_date(issue_date)
        due_date = self.validate_date(due_date)
        status = self.validate_string(status)
        fine_amount = self.validate_integer(fine_amount)
        paid_amount = self.validate_integer(paid_amount)
        payment_date = self.validate_date(payment_date)

        self.patron_id = patron_id
        self.loan_id = loan_id
        self.amount = amount
        self.issue_date = issue_date
        self.due_date = due_date
        self.status = status
        self.fine_amount = fine_amount
        self.paid_amount = paid_amount
        self.payment_date = payment_date

    def validate_integer(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid integer value")
        return value

    def validate_string(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid string value")
        return value

    def validate_date(self, value):
        if not isinstance(value, date):
            raise ValueError("Invalid date value")
        return value

engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

try:
    fine = Fine(1, 1, "10.00", date(2022, 1, 1), date(2022, 1, 15), "pending", 10, 0, None)
    session.add(fine)
    session.commit()
except IntegrityError as e:
    print("Integrity error: ", e)
except InvalidRequestError as e:
    print("Invalid request error: ", e)
except ValueError as e:
    print("Value error: ", e)