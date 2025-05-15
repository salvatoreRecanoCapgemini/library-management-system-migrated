

from datetime import date

class EventRegistration:
    def __init__(self, event_id, patron_id, registration_date, attendance_status):
        self.id = None
        self.event_id = event_id
        self.patron_id = patron_id
        self.registration_date = registration_date
        self.attendance_status = attendance_status

    def __repr__(self):
        return f"EventRegistration(id={self.id}, event_id={self.event_id}, patron_id={self.patron_id}, registration_date={self.registration_date}, attendance_status={self.attendance_status})"