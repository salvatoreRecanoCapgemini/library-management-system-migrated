

from sqlalchemy import select, join
from models import Program, Registration, Patron
import logging

def get_program_metrics(program_id):
    if not isinstance(program_id, int) or program_id <= 0:
        raise ValueError("Invalid program_id")

    try:
        query = select([Program, Registration, Patron]).select_from(join(Program, Registration, Program.program_id == Registration.program_id)).select_from(join(Registration, Patron, Registration.patron_id == Patron.patron_id)).filter(Registration.payment_status.in_(['PAID', 'PARTIALLY_PAID']))
        results = query.execute().fetchall()
    except Exception as e:
        logging.error(f"Database query failed: {e}")
        return None

    if not results:
        return {'program_id': program_id, 'total_registrations': 0, 'total_attendees': 0, 'total_revenue': 0, 'average_attendance_rate': 0}

    total_registrations = len(results)
    total_attendees = sum(1 for result in results if result.attendance_log)
    total_revenue = sum(result.cost for result in results)
    average_attendance_rate = total_attendees / total_registrations if total_registrations > 0 else 0
    return {'program_id': program_id, 'total_registrations': total_registrations, 'total_attendees': total_attendees, 'total_revenue': total_revenue, 'average_attendance_rate': average_attendance_rate}