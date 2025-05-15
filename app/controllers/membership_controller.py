

from app.services.membership_service import MembershipService
from app.services.notification_service import NotificationService

class MembershipController:
    def process_membership_renewals_and_notifications(self):
        membership_service = MembershipService()
        membership_service.process_membership_renewals_and_notifications()

    def send_notification(self, patron, notification_message):
        if not patron or not notification_message:
            raise ValueError("Patron and notification message are required")

        try:
            notification_service = NotificationService()
            notification_service.send_notification(patron, notification_message)
        except Exception as e:
            # Handle the exception, for example, log the error
            print(f"Error sending notification: {str(e)}")