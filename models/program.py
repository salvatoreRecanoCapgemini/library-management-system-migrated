

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

Base = declarative_base()

class Program(Base):
    __tablename__ = 'programs'

    program_id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum('PUBLISHED', 'IN_PROGRESS', 'CANCELLED', 'COMPLETED'))
    session_schedule = Column(String)
    minimum_participants = Column(Integer)

    __table_args__ = (CheckConstraint('minimum_participants > 0', name='check_minimum_participants_positive'),)

    registrations = relationship('Registration', backref='program')
    audit_logs = relationship('AuditLog', backref='program')