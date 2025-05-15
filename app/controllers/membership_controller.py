

from datetime import datetime, timedelta
from typing import List
import logging

class MembershipController:
    def __init__(self, membership_service, notification_service):
        self.membership_service = membership_service
        self.notification_service = notification_service
        self.logger = logging.getLogger(__name__)

    def process_renewals(self):
        try:
            if not self.membership_service or not self.notification_service:
                self.logger.error("Membership service or notification service is not initialized")
                return
            expiring_memberships = self.membership_service.get_expiring_memberships()
            for membership in expiring_memberships:
                self.membership_service.renew_membership(membership)
        except Exception as e:
            self.logger.error(f"Error processing renewals: {str(e)}")

    def send_notifications(self):
        try:
            if not self.membership_service or not self.notification_service:
                self.logger.error("Membership service or notification service is not initialized")
                return
            patrons = self.membership_service.get_patrons_with_expiring_memberships()
            for patron in patrons:
                self.notification_service.send_notification(patron)
        except Exception as e:
            self.logger.error(f"Error sending notifications: {str(e)}")