

from datetime import datetime
from typing import Dict
from sqlalchemy.exc import SQLAlchemyError

class AuditLogRepository:
    def __init__(self, db_session):
        if db_session is None:
            raise ValueError("db_session cannot be None")
        self.db_session = db_session

    def log_notification(self, membership_id: int, notification_text: str) -> None:
        if membership_id is None or membership_id <= 0:
            raise ValueError("membership_id must be a positive integer")
        if notification_text is None or len(notification_text.strip()) == 0:
            raise ValueError("notification_text must be a non-empty string")

        try:
            log_entry = self.create_log_entry(membership_id, notification_text)
            self.save_log_entry(log_entry)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def create_log_entry(self, membership_id: int, notification_text: str) -> Dict:
        try:
            return {
                'membership_id': membership_id,
                'notification_text': notification_text,
                'created_at': datetime.now()
            }
        except Exception as e:
            raise e

    def save_log_entry(self, log_entry: Dict) -> None:
        try:
            self.db_session.add(log_entry)
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e