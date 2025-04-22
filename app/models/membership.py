

from datetime import datetime

class Membership:
    def __init__(self, membership_id, patron_id, plan_id, end_date, auto_renewal, payment_processing_result=None):
        self.membership_id = membership_id
        self.patron_id = patron_id
        self.plan_id = plan_id
        if isinstance(end_date, str):
            try:
                self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid date format. Date should be in YYYY-MM-DD format.")
        elif isinstance(end_date, datetime):
            self.end_date = end_date
        else:
            raise ValueError("Invalid date type. Date should be a string or a datetime object.")
        if not isinstance(auto_renewal, bool):
            raise ValueError("Auto-renewal status should be a boolean value.")
        self.auto_renewal = auto_renewal
        self.payment_processing_result = payment_processing_result

    def __str__(self):
        return f"Membership ID: {self.membership_id}, Patron ID: {self.patron_id}, Plan ID: {self.plan_id}, End Date: {self.end_date}, Auto Renewal: {self.auto_renewal}, Payment Processing Result: {self.payment_processing_result}"