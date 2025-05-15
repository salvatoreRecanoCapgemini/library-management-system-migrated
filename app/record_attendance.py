

from flask import current_app
from app import db
from app.models import Program, Registration, Notification
import logging

def record_attendance(program_id, registration_id):
    try:
        program_data = Program.query.get(program_id)
        if program_data.status != 'IN_PROGRESS':
            raise Exception('Invalid program status')

        attendance_records = Registration.query.filter_by(program_id=program_id).all()
        for registration in attendance_records:
            if registration.attendance_log.get('status') != 'PRESENT':
                registration.attendance_log = {'status': 'PRESENT'}
                db.session.add(registration)

        db.session.commit()

        for registration in attendance_records:
            notification = Notification(registration_id=registration.id, message=f'Attendance recorded for {program_data.name}')
            db.session.add(notification)

        db.session.commit()

        logging.info(f'Attendance recorded for program {program_id} with registrations: {[r.id for r in attendance_records]}')

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error recording attendance for program {program_id}: {str(e)}')
        raise