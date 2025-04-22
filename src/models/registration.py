

from typing import List

class AttendanceLog:
    def __init__(self, log_id: int, attendance_date: str, attended: bool):
        self.log_id = log_id
        self.attendance_date = attendance_date
        self.attended = attended

class Registration:
    def __init__(self, registration_id: int, program_id: int, patron_id: int, payment_status: str, attendance_log: List[AttendanceLog]):
        self.registration_id = registration_id
        self.program_id = program_id
        self.patron_id = patron_id
        self.payment_status = payment_status
        self.attendance_log = attendance_log