

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_log'
    log_id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(JSON)
    program_id = Column(Integer, ForeignKey('library_programs.program_id'))

    loan = relationship('Loan', backref='audit_log')
    program = relationship('LibraryProgram', backref='audit_log')