

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class AuditLog(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, nullable=False)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(100), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)
    action_timestamp = db.Column(db.DateTime, nullable=False)
    log_date = db.Column(db.DateTime, nullable=False)
    new_values = db.Column(db.JSON, nullable=False)

    def __init__(self, log_id, program_id, action, log_date, table_name, record_id, action_type, action_timestamp, new_values):
        if not isinstance(log_id, int) or not isinstance(program_id, int) or not isinstance(record_id, int):
            raise ValueError("log_id, program_id, and record_id must be integers")
        if not isinstance(action, str) or not isinstance(table_name, str) or not isinstance(action_type, str):
            raise ValueError("action, table_name, and action_type must be strings")
        if not isinstance(log_date, datetime) or not isinstance(action_timestamp, datetime):
            raise ValueError("log_date and action_timestamp must be datetime objects")
        if not isinstance(new_values, dict):
            raise ValueError("new_values must be a dictionary")
        self.log_id = log_id
        self.program_id = program_id
        self.action = action
        self.log_date = log_date
        self.table_name = table_name
        self.record_id = record_id
        self.action_type = action_type
        self.action_timestamp = action_timestamp
        self.new_values = new_values

    def __repr__(self):
        return f"AuditLog(log_id={self.log_id}, program_id={self.program_id}, action={self.action}, log_date={self.log_date}, table_name={self.table_name}, record_id={self.record_id}, action_type={self.action_type}, action_timestamp={self.action_timestamp}, new_values={self.new_values})"

    def log_notification(self):
        try:
            existing_log = AuditLog.query.filter_by(log_id=self.log_id).first()
            if existing_log:
                raise ValueError("Log entry already exists")
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e