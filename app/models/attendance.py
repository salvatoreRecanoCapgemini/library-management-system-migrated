

from typing import Optional

class Attendance:
    def __init__(self, attendance_id: int, program_id: int, registration_id: int, attendance_status: str):
        if not isinstance(attendance_id, int):
            raise TypeError("attendance_id must be an integer")
        if not isinstance(program_id, int):
            raise TypeError("program_id must be an integer")
        if not isinstance(registration_id, int):
            raise TypeError("registration_id must be an integer")
        if not isinstance(attendance_status, str):
            raise TypeError("attendance_status must be a string")

        self.attendance_id = attendance_id
        self.program_id = program_id
        self.registration_id = registration_id
        self.attendance_status = attendance_status

    def __str__(self):
        return f"Attendance(attendance_id={self.attendance_id}, program_id={self.program_id}, registration_id={self.registration_id}, attendance_status='{self.attendance_status}')"

    def __repr__(self):
        return self.__str__()