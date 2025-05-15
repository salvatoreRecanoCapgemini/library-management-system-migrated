

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Attendance, AttendanceLog

class AttendanceRepository:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.db = Session()

    def retrieve_attendance_records(self, program_id):
        if program_id is None:
            raise ValueError("Program ID is required")
        try:
            attendance_records = self.db.query(Attendance).filter_by(program_id=program_id).all()
            return attendance_records
        except Exception as e:
            self.db.rollback()
            raise e

    def update_attendance_log(self, registration_id, attendance_status):
        if registration_id is None or attendance_status is None:
            raise ValueError("Registration ID and attendance status are required")
        try:
            attendance_log = self.db.query(AttendanceLog).filter_by(registration_id=registration_id).first()
            if attendance_log is None:
                raise ValueError("Attendance log not found")
            attendance_log.attendance_status = attendance_status
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e