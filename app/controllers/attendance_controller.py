

from app.services.attendance_service import AttendanceService

class AttendanceController:
    def record_attendance(self, program_id, registration_id):
        """
        Records attendance for a given program and registration.

        Args:
            program_id (int): The ID of the program.
            registration_id (int): The ID of the registration.

        Raises:
            ValueError: If program_id or registration_id is invalid.
            AttributeError: If AttendanceService does not have a record_attendance method.
            Exception: If any other error occurs during attendance recording.
        """
        if not isinstance(program_id, int) or not isinstance(registration_id, int):
            raise ValueError("Invalid program_id or registration_id")

        attendance_service = AttendanceService()
        if not hasattr(attendance_service, 'record_attendance'):
            raise AttributeError("AttendanceService does not have a record_attendance method")

        try:
            attendance_service.record_attendance(program_id, registration_id)
        except Exception as e:
            raise Exception("Error recording attendance: {}".format(str(e)))