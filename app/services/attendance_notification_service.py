

from app.models import Notification, db

class AttendanceNotificationService:
    """
    A service class responsible for generating attendance notifications.
    """

    def generate_attendance_notification(self, registration_id, attendance_status):
        """
        Generates an attendance notification for the given registration ID and attendance status.

        Args:
            registration_id (int): The ID of the registration.
            attendance_status (str): The attendance status.

        Raises:
            ValueError: If the registration ID or attendance status is invalid.
            Exception: If an error occurs while generating the notification.
        """
        if not isinstance(registration_id, int) or registration_id <= 0:
            raise ValueError("Invalid registration ID")
        if not isinstance(attendance_status, str) or not attendance_status.strip():
            raise ValueError("Invalid attendance status")

        try:
            notification = Notification(registration_id, attendance_status)
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception("Error generating attendance notification") from e