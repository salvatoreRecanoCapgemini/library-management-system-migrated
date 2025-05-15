

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Program, Registration, Patron
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime
import logging
import threading

engine = create_engine('postgresql://user:password@host:port/dbname')
Session = sessionmaker(bind=engine)

lock = threading.Lock()

def manage_program_lifecycle(program_id, action, params):
    session = Session()
    try:
        with lock:
            if action == 'START_PROGRAM':
                start_program(program_id, session)
            elif action == 'RECORD_ATTENDANCE':
                record_attendance(program_id, params, session)
            elif action == 'COMPLETE_PROGRAM':
                complete_program(program_id, session)
            else:
                raise ValueError('Invalid action')
            session.commit()
    except IntegrityError as e:
        session.rollback()
        raise e
    except OperationalError as e:
        session.rollback()
        logging.error(f"Operational error: {e}")
    finally:
        session.close()

def start_program(program_id, session):
    program = session.query(Program).get(program_id)
    if program.status != 'PUBLISHED':
        raise ValueError('Program is not in published status')
    if len(program.registrations) < program.min_registrations:
        raise ValueError('Program does not have sufficient registrations')
    program.session_schedule = datetime.now()
    program.status = 'IN_PROGRESS'

def record_attendance(program_id, params, session):
    if not params or 'attendance' not in params:
        raise ValueError('Invalid params')
    program = session.query(Program).get(program_id)
    if program.status != 'IN_PROGRESS':
        raise ValueError('Invalid program status')
    attendance_records = session.query(Registration).filter_by(program_id=program_id).all()
    for record in attendance_records:
        record.attendance = params.get('attendance', False)
    for record in attendance_records:
        if record.attendance:
            # Send notification to patron
            send_notification(record.patron_id)

def complete_program(program_id, session):
    program = session.query(Program).get(program_id)
    if program.status != 'IN_PROGRESS':
        raise ValueError('Invalid program status')
    completion_statistics = {}
    for registration in program.registrations:
        completion_statistics[registration.patron_id] = registration.attendance
    for registration in program.registrations:
        registration.status = 'COMPLETED' if registration.attendance else 'INCOMPLETE'
    program.status = 'COMPLETED'

def send_notification(patron_id):
    # Implement notification sending logic here
    pass