

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging
import json

log = logging.getLogger(__name__)

engine = create_engine('postgresql://user:password@host:port/dbname')
Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_log'
    log_id = Column(Integer, primary_key=True)
    table_name = Column(String)
    record_id = Column(Integer)
    action_type = Column(String)
    action_timestamp = Column(DateTime)
    new_values = Column(JSON)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def create_audit_log(notification_message, loan_id):
    try:
        if not isinstance(notification_message, dict):
            notification_message = json.loads(notification_message)
        if not isinstance(loan_id, int):
            raise ValueError("Loan ID must be an integer")
        session = Session()
        log = AuditLog(table_name='notifications', record_id=None, action_type='INSERT', action_timestamp=datetime.now(), new_values=notification_message)
        session.add(log)
        session.commit()
    except Exception as e:
        log.error(e)

def insert_into_audit_log(table_name, record_id, action_type, action_timestamp, new_values):
    try:
        if not isinstance(table_name, str) or not table_name.isalnum():
            raise ValueError("Table name must be a valid string")
        if not isinstance(record_id, int):
            raise ValueError("Record ID must be an integer")
        if not isinstance(action_type, str) or action_type not in ['INSERT', 'UPDATE', 'DELETE']:
            raise ValueError("Action type must be one of INSERT, UPDATE, DELETE")
        if not isinstance(action_timestamp, datetime):
            raise ValueError("Action timestamp must be a datetime object")
        if not isinstance(new_values, dict):
            new_values = json.loads(new_values)
        session = Session()
        log = AuditLog(table_name=table_name, record_id=record_id, action_type=action_type, action_timestamp=action_timestamp, new_values=new_values)
        session.add(log)
        session.commit()
        return True
    except Exception as e:
        log.error(e)
        return False