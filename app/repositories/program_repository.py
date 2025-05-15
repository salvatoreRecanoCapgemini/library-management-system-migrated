

import sqlite3
from typing import Tuple, Dict

class ProgramRepository:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_program(self, program_id: int) -> Tuple:
        try:
            if not isinstance(program_id, int) or program_id <= 0:
                raise ValueError("Invalid program_id")
            self.cursor.execute('SELECT * FROM library_programs WHERE program_id = ?', (program_id,))
            program_data = self.cursor.fetchone()
            if program_data is None:
                raise ValueError("Program not found")
            return program_data
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            self.close_connection()

    def update_program_status(self, program_id: int, status: str) -> None:
        try:
            if not isinstance(program_id, int) or program_id <= 0:
                raise ValueError("Invalid program_id")
            if status not in ["active", "inactive", "pending"]:
                raise ValueError("Invalid status")
            self.cursor.execute('UPDATE library_programs SET status = ? WHERE program_id = ?', (status, program_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            self.close_connection()

    def record_attendance(self, program_id: int, attendance_record: Dict) -> None:
        try:
            if not isinstance(program_id, int) or program_id <= 0:
                raise ValueError("Invalid program_id")
            if not isinstance(attendance_record, dict):
                raise ValueError("Invalid attendance_record")
            self.cursor.execute('INSERT INTO attendance_records (program_id, attendance_record) VALUES (?, ?)', (program_id, str(attendance_record)))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            self.close_connection()

    def close_connection(self) -> None:
        self.conn.close()