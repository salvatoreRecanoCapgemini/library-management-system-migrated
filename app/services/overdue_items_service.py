

from datetime import datetime, timedelta
from typing import List

class Loan:
    def __init__(self, id: int, due_date: datetime, status: str):
        self.id = id
        self.due_date = due_date
        self.status = status

class Fine:
    def __init__(self, loan_id: int, amount: float):
        self.loan_id = loan_id
        self.amount = amount

class Notification:
    def __init__(self, patron_id: int, message: str):
        self.patron_id = patron_id
        self.message = message

class AuditLog:
    def __init__(self):
        self.notifications = []

    def record_notification(self, notification: Notification):
        self.notifications.append(notification)

class OverdueItemsService:
    def __init__(self, loans: List[Loan], audit_log: AuditLog):
        self.loans = loans
        self.audit_log = audit_log
        self.notifications = []

    def retrieve_active_loans(self) -> List[Loan]:
        return [loan for loan in self.loans if loan.status == 'ACTIVE' and loan.due_date < datetime.now()]

    def process_overdue_items(self):
        active_loans = self.retrieve_active_loans()
        for loan in active_loans:
            if loan.status != 'OVERDUE':
                fine_amount = self.calculate_fine_amount(loan)
                fine = Fine(loan.id, fine_amount)
                loan.status = 'OVERDUE'
                notification = self.construct_notification(loan)
                self.store_notification(notification)

        self.process_notifications()

    def calculate_fine_amount(self, loan: Loan) -> float:
        if loan.due_date >= datetime.now():
            return 0
        days_overdue = (datetime.now() - loan.due_date).days
        return days_overdue * 0.1

    def construct_notification(self, loan: Loan) -> Notification:
        message = f'Loan {loan.id} is overdue. Please return the item.'
        return Notification(loan.id, message)

    def store_notification(self, notification: Notification):
        self.notifications.append(notification)

    def process_notifications(self):
        for notification in self.notifications:
            self.audit_log.record_notification(notification)

    def release_notifications(self):
        self.notifications = []