

import logging
from typing import Dict, List

from sqlalchemy import create_engine, create_engine, text
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

Base = declarative_base()

class ProgramStatus(Base):
    __tablename__ = 'program_status'
    program_id = Column(Integer, primary_key=True)
    status = Column(String)
    registrations = Column(Integer)
    min_participants = Column(Integer)

class AttendanceRecord(Base):
    __tablename__ = 'attendance_records'
    program_id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, primary_key=True)
    attendance = Column(Boolean)

class ProgramMetric(Base):
    __tablename__ = 'program_metrics'
    program_id = Column(Integer, primary_key=True)
    metric = Column(String)
    value = Column(Integer)

engine = create_engine('postgresql://user:password@host:port/dbname')
Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))

class ProgramService:
    def manage_program_lifecycle(self, program_id: int, action: str, params: Dict) -> None:
        program_status = self.query_database('SELECT * FROM program_status WHERE program_id = %s', (program_id,))
        program_details = program_status[0]
        if action == 'START_PROGRAM':
            self.start_program(program_details)
        elif action == 'RECORD_ATTENDANCE':
            self.record_attendance(program_details, params)
        elif action == 'COMPLETE_PROGRAM':
            self.complete_program(program_details)
        else:
            raise ValueError('Invalid action')
        self.log_program_state_change(program_id, action, params)

    def start_program(self, program: Dict) -> None:
        if program['status'] != 'PUBLISHED':
            raise ValueError('Program is not in the PUBLISHED status')
        if program['registrations'] < program['min_participants']:
            self.create_waitlist_notification_batch(program)
            self.update_program_status(program, 'CANCELLED')
        self.initialize_session_schedule(program)
        self.update_program_status(program, 'IN_PROGRESS')

    def record_attendance(self, program: Dict, params: Dict) -> None:
        if program['status'] != 'IN_PROGRESS':
            raise ValueError('Program is not in the IN_PROGRESS status')
        attendance_records = self.get_attendance_records(program)
        for registration in attendance_records:
            self.update_attendance_log(registration, params)
        self.generate_attendance_notification(program, params)

    def complete_program(self, program: Dict) -> None:
        if program['status'] != 'IN_PROGRESS':
            raise ValueError('Program is not in the IN_PROGRESS status')
        completion_statistics = self.calculate_completion_statistics(program)
        self.update_completion_status(program, completion_statistics)
        self.update_program_status(program, 'COMPLETED')

    def log_program_state_change(self, program_id: int, action: str, params: Dict) -> None:
        logging.info(f'Program {program_id} state changed to {action} with params {params}')

    def get_program_metrics(self, program_id: int) -> List[Dict]:
        program_metrics = self.query_database('SELECT * FROM program_metrics WHERE program_id = %s', (program_id,))
        return program_metrics

    def query_database(self, query: str, params: tuple) -> List[Dict]:
        with Session() as session:
            result = session.execute(text(query), params)
            return [dict(row) for row in result]

    def create_waitlist_notification_batch(self, program: Dict) -> None:
        # Create a notification batch for waitlisted registrations
        with Session() as session:
            for registration in program['registrations']:
                if registration['status'] == 'WAITLISTED':
                    notification = Notification(registration_id=registration['id'], program_id=program['id'])
                    session.add(notification)
            session.commit()

    def initialize_session_schedule(self, program: Dict) -> None:
        # Initialize the session schedule for the program
        with Session() as session:
            for session in program['sessions']:
                session_schedule = SessionSchedule(program_id=program['id'], session_id=session['id'])
                session.add(session_schedule)
            session.commit()

    def update_program_status(self, program: Dict, status: str) -> None:
        # Update the program status
        with Session() as session:
            program_status = session.query(ProgramStatus).filter_by(program_id=program['id']).first()
            program_status.status = status
            session.commit()

    def get_attendance_records(self, program: Dict) -> List[Dict]:
        # Retrieve attendance records for the program
        with Session() as session:
            attendance_records = session.query(AttendanceRecord).filter_by(program_id=program['id']).all()
            return [dict(record) for record in attendance_records]

    def update_attendance_log(self, registration: Dict, params: Dict) -> None:
        # Update the attendance log for the registration
        with Session() as session:
            attendance_log = session.query(AttendanceLog).filter_by(registration_id=registration['id']).first()
            attendance_log.attendance = params['attendance']
            session.commit()

    def generate_attendance_notification(self, program: Dict, params: Dict) -> None:
        # Generate an attendance notification for the program
        with Session() as session:
            notification = Notification(program_id=program['id'], params=params)
            session.add(notification)
            session.commit()

    def calculate_completion_statistics(self, program: Dict) -> Dict:
        # Calculate completion statistics for the program
        with Session() as session:
            completion_statistics = session.query(CompletionStatistics).filter_by(program_id=program['id']).first()
            return dict(completion_statistics)

    def update_completion_status(self, program: Dict, completion_statistics: Dict) -> None:
        # Update the completion status for the program
        with Session() as session:
            completion_status = session.query(CompletionStatus).filter_by(program_id=program['id']).first()
            completion_status.status = completion_statistics['status']
            session.commit()