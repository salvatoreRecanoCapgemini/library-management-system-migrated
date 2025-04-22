

from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_log'

    log_id = Column(Integer, primary_key=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action_type = Column(Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False, validate='immutable')
    action_timestamp = Column(TIMESTAMP, nullable=False)
    new_values = Column(JSON, nullable=False)

    program_id = Column(Integer, ForeignKey('program.id'), nullable=False)
    program = relationship('Program', backref='audit_logs')

    patron_id = Column(Integer, ForeignKey('patron.id'), nullable=False)
    patron = relationship('Patron', backref='audit_logs')