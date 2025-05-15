

from datetime import date, timedelta
from audit_log import log_notification
from payment_processing import attempt_payment_processing, payment_successful
from patron_membership import PatronMembership, create_new_membership_period, update_old_membership_status

def process_membership_renewals():
    expiring_memberships = PatronMembership.query.filter(PatronMembership.end_date <= date.today() + timedelta(days=7)).all()
    for membership in expiring_memberships:
        if membership.auto_renewal and not membership.patron.fines and not membership.patron.loans and not membership.renewed:
            payment_result = attempt_payment_processing(membership)
            if payment_result:
                create_new_membership_period(membership)
                update_old_membership_status(membership)
                log_notification(membership, "Membership renewed successfully")
            else:
                log_notification(membership, "Payment processing failed")
        else:
            if membership.auto_renewal and (membership.patron.fines or membership.patron.loans):
                log_notification(membership, "Membership not renewed due to outstanding fines or loans")
            elif membership.renewed:
                log_notification(membership, "Membership already renewed")
            else:
                log_notification(membership, "Membership not renewed")