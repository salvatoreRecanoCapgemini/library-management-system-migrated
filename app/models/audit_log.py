

from datetime import datetime
from app import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String)
    record_id = db.Column(db.Integer)
    action_type = db.Column(db.String)
    action_timestamp = db.Column(db.DateTime)
    new_values = db.Column(db.String)
    fine = db.relationship('Fine', backref='audit_log')

    def __init__(self, log_id, table_name, record_id, action_type, action_timestamp, new_values):
        self.log_id = log_id
        self.table_name = table_name
        self.record_id = record_id
        self.action_type = action_type
        self.action_timestamp = action_timestamp
        self.new_values = new_values

    def insert_into_audit_log(self, table_name, record_id, action_type, action_timestamp, new_values):
        try:
            audit_log = AuditLog(
                log_id=None,
                table_name=table_name,
                record_id=record_id,
                action_type=action_type,
                action_timestamp=action_timestamp,
                new_values=new_values
            )
            db.session.add(audit_log)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e