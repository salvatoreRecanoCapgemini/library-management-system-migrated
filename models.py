

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, DateTime, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import date

Base = declarative_base()

class LibraryEvent(Base):
    __tablename__ = 'library_events'
    event_id = Column(Integer, primary_key=True)
    title = Column(String)
    event_date = Column(Date)
    status = Column(String)

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    registration_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('library_events.event_id'))
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    attendance_status = Column(String)
    event = relationship("LibraryEvent", backref="event_registrations")
    patron = relationship("Patron", backref="event_registrations")

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    membership_date = Column(Date, default=date.today())
    status = Column(String, default='ACTIVE')
    birth_date = Column(Date)
    fines = relationship("Fine", backref="patron")
    loans = relationship("Loan", backref="patron")

    @classmethod
    def create_patron(cls, first_name, last_name, email, phone, birth_date):
        patron = cls(first_name=first_name, last_name=last_name, email=email, phone=phone, birth_date=birth_date)
        return patron

class PatronMembership(Base):
    __tablename__ = 'patron_memberships'
    membership_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    plan_id = Column(Integer, ForeignKey('membership_plans.plan_id'))
    end_date = Column(Date)
    auto_renewal = Column(Boolean)
    status = Column(String)
    patron = relationship("Patron", backref="patron_memberships")
    plan = relationship("MembershipPlan", backref="patron_memberships")

class MembershipPlan(Base):
    __tablename__ = 'membership_plans'
    plan_id = Column(Integer, primary_key=True)
    price = Column(Float)
    duration_months = Column(Integer)

class Fine(Base):
    __tablename__ = 'fines'
    fine_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    status = Column(String)

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'))
    status = Column(String)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    log_id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(JSONB)