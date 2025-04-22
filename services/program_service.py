

from models import Program, Registration, Patron, AuditLog
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///attendance.db')
Base = declarative_base()

class AttendanceRecord(Base):
    __tablename__ = 'attendance_records'
    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer)
    attendance = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class ProgramService:
    def start_program(self, program_id):
        program = Program.get(program_id)
        if program.status != 'published':
            raise ValueError('Program is not in published status')
        if len(Registration.get_by_program_id(program_id, status='paid')) < program.min_required_registrations:
            raise ValueError('Minimum required registrations not met')
        program.initialize_session_schedule()
        program.status = 'in_progress'
        program.save()
        AuditLog.log('Program started', program_id)

    def record_attendance(self, program_id):
        program = Program.get(program_id)
        if program.status != 'in_progress':
            raise ValueError('Program is not in progress')
        attendance_records = []
        # Create a temporary table for attendance processing
        temp_table = session.query(AttendanceRecord).filter_by(registration_id=Registration.get_by_program_id(program_id))
        # Retrieve attendance records
        attendance_records = temp_table.all()
        for record in attendance_records:
            registration = Registration.get(record.registration_id)
            registration.attendance_log.append(record)
            registration.save()
            # Generate attendance notifications for each registration
            # Add implementation for generating attendance notifications
        # Drop the temporary table for attendance records
        session.query(AttendanceRecord).delete()

    def complete_program(self, program_id):
        program = Program.get(program_id)
        if program.status != 'in_progress':
            raise ValueError('Program is not in progress')
        # Calculate completion statistics
        completion_stats = {}
        for registration in Registration.get_by_program_id(program_id):
            if registration.attendance_log:
                completion_stats[registration.patron_id] = True
            else:
                completion_stats[registration.patron_id] = False
        # Update completion status for participants
        for patron_id, completed in completion_stats.items():
            patron = Patron.get(patron_id)
            patron.program_completion_status = completed
            patron.save()
        program.status = 'completed'
        program.save()
        AuditLog.log('Program completed', program_id)