

from datetime import datetime, timedelta
from typing import List, Dict

class MembershipService:
    def __init__(self, payment_gateway, notification_service, audit_log_service, notification_service):
        self.payment_gateway = payment_gateway
        self.audit_log_service = audit_log_service
        self.notification_service = notification_service

    def process_expiring_memberships(self, expiring_memberships: List[Dict]):
        notifications = []
        for membership in expiring_memberships:
            if membership['auto_renewal'] and not membership['patron']['pending_fines'] and not membership['patron']['overdue_items']:
                payment_result = self.payment_gateway.process_payment(membership['payment_method'], membership['amount'])
                if payment_result['success']:
                    new_membership_period = self.create_new_membership_period(membership)
                    self.update_old_membership_status(membership, 'EXPIRED')
                    notification = self.prepare_notification_for_successful_auto_renewal(membership, new_membership_period)
                    notifications.append(notification)
                else:
                    notification = self.prepare_notification_for_manual_renewal(membership)
                    notifications.append(notification)
        self.log_notifications(notifications)

    def create_new_membership_period(self, membership: Dict) -> Dict:
        new_membership_period = {
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=membership['duration_in_days']),
            'membership_id': membership['id']
        }
        return new_membership_period

    def update_old_membership_status(self, membership: Dict, status: str):
        membership['status'] = status

    def prepare_notification_for_successful_auto_renewal(self, membership: Dict, new_membership_period: Dict) -> Dict:
        notification = {
            'type': 'successful_auto_renewal',
            'membership_id': membership['id'],
            'new_membership_period': new_membership_period,
            'message': f'Membership {membership["id"]} has been successfully auto-renewed.'
        }
        return notification

    def prepare_notification_for_manual_renewal(self, membership: Dict) -> Dict:
        notification = {
            'type': 'manual_renewal',
            'membership_id': membership['id'],
            'message': f'Membership {membership["id"]} requires manual renewal.'
        }
        return notification

    def log_notifications(self, notifications: List[Dict]):
        for notification in notifications:
            self.audit_log_service.create_audit_log_entry(notification)
            self.notification_service.send_notification(notification)