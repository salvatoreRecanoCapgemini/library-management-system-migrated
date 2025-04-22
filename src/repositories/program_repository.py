

package src.repositories;

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.models import Program, AuditLog
from sqlalchemy.exc import SQLAlchemyError

class ProgramRepository:
    def __init__(self, db_session):
        if not db_session:
            raise ValueError("db_session is required")
        self.db_session = db_session

    def get_program_status(self, program_id):
        if not program_id:
            raise ValueError("program_id is required")
        try:
            query = self.db_session.query(Program.status).filter(Program.program_id == program_id)
            return query.first()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def create_temp_table_for_program_status(self, program_id):
        if not program_id:
            raise ValueError("program_id is required")
        try:
            create_temp_table_query = f"""
                CREATE TEMPORARY TABLE temp_program_status_{program_id} AS
                SELECT * FROM program_status WHERE program_id = :program_id
            """
            self.db_session.execute(create_temp_table_query, {'program_id': program_id})
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def get_program_details(self, program_id):
        if not program_id:
            raise ValueError("program_id is required")
        try:
            query = self.db_session.query(Program).filter(Program.program_id == program_id)
            return query.first()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def log_program_state_change(self, program_id, action, params):
        if not program_id:
            raise ValueError("program_id is required")
        if not action:
            raise ValueError("action is required")
        if not params:
            raise ValueError("params are required")
        try:
            audit_log = AuditLog('program', program_id, 'UPDATE', datetime.now(), {'action': action, 'params': params})
            self.db_session.add(audit_log)
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e