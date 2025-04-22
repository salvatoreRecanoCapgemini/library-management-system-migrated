

from datetime import date
from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint

Base = declarative_base()

class Fine(Base):
    __tablename__ = 'fines'
    __table_args__ = (UniqueConstraint('fine_id', name='_fine_id_unique_constraint'),)

    fine_id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    payment_date = Column(Date, nullable=True)

    def process_payment(self, paid_amount):
        if paid_amount <= 0:
            raise Exception('Paid amount must be a positive number')
        if self.status != 'PENDING':
            raise Exception('Valid unpaid fine not found')
        remaining_amount = self.amount - paid_amount
        if remaining_amount < 0:
            raise Exception('Partial payments not supported')
        if remaining_amount == 0:
            self.status = 'PAID'
            self.payment_date = date.today()
        elif remaining_amount > 0:
            self.status = 'PARTIALLY_PAID'
            self.payment_date = date.today()