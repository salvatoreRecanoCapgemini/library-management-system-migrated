

from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import relationship
from sqlalchemy.orm import backref
from .fine import Fine
from .loan import Loan
from .registration import Registration

Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    fines = relationship('Fine', backref=backref('patron', lazy=True))
    loans = relationship('Loan', backref=backref('patron', lazy=True))
    status = Column(String)
    active_loans = Column(Integer)
    phone = Column(String)
    membership_date = Column(Date)
    birth_date = Column(Date)

    def __init__(self, email, first_name, last_name):
        if not email or not first_name or not last_name:
            raise ValueError("Email, first name, and last name are required")
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def has_pending_fines(self):
        """
        Check if the patron has any pending fines
        """
        return self.fines.filter(Fine.status == 'PENDING').first() is not None

    def has_overdue_items(self):
        """
        Check if the patron has any overdue items
        """
        return self.loans.filter(Loan.status == 'OVERDUE').first() is not None

    registrations = relationship('Registration', backref=backref('patron', lazy=True))