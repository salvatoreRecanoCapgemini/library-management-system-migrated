

from datetime import datetime, timedelta
from random import random
from yourapplication import db
from yourapplication.models import PatronMembership, Patron, MembershipPlan, Fine, Loan, AuditLog

def process_membership_renewals_and_notifications():
    expiring_memberships = []

    for membership in PatronMembership.query.all():
        if membership.status == 'ACTIVE' and membership.end_date <= datetime.now() + timedelta(days=7):
            patron = Patron.query.get(membership.patron_id)
            plan = MembershipPlan.query.get(membership.plan_id)

            if Fine.query.filter_by(patron_id=patron.patron_id, status='PENDING').first() or Loan.query.filter_by(patron_id=patron.patron_id, status='OVERDUE').first():
                continue

            expiring_memberships.append({'membership_id': membership.membership_id, 'patron_id': patron.patron_id, 'plan_id': plan.plan_id, 'end_date': membership.end_date, 'auto_renewal': membership.auto_renewal, 'patron': patron})

    for membership in expiring_memberships:
        if membership['auto_renewal'] and not Fine.query.filter_by(patron_id=membership['patron_id'], status='PENDING').first() and not Loan.query.filter_by(patron_id=membership['patron_id'], status='OVERDUE').first():
            if random() < 0.5:
                new_membership = PatronMembership(membership_id=membership['membership_id'], patron_id=membership['patron_id'], plan_id=membership['plan_id'], end_date=datetime.now() + timedelta(days=membership['plan_id'].duration_months * 30), auto_renewal=membership['auto_renewal'], status='ACTIVE')
                db.session.add(new_membership)
                db.session.commit()

                old_membership = PatronMembership.query.get(membership['membership_id'])
                old_membership.status = 'EXPIRED'
                db.session.commit()

                notification = AuditLog(table_name='membership_notifications', record_id=membership['membership_id'], action_type='NOTIFICATION', action_timestamp=datetime.now(), new_values={'email': membership['patron'].email, 'message': 'Membership renewed successfully', 'renewal_status': 'SUCCESS', 'new_membership_id': new_membership.membership_id})
                db.session.add(notification)
                db.session.commit()
            else:
                notification = AuditLog(table_name='membership_notifications', record_id=membership['membership_id'], action_type='NOTIFICATION', action_timestamp=datetime.now(), new_values={'email': membership['patron'].email, 'message': 'Membership renewal failed', 'renewal_status': 'FAILURE'})
                db.session.add(notification)
                db.session.commit()