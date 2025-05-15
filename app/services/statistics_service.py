

from datetime import datetime, timedelta
from app.models import AuditLog
from app.repositories import LoanRepository, FineRepository, BookRepository, EventRepository

class StatisticsService:
    def generate_monthly_report(self, p_year, p_month):
        try:
            if not isinstance(p_year, int) or not isinstance(p_month, int):
                raise ValueError("Year and month must be integers")
            if p_month < 1 or p_month > 12:
                raise ValueError("Month must be between 1 and 12")

            start_date = self.calculate_start_date(p_year, p_month)
            end_date = self.calculate_end_date(p_year, p_month)

            loan_stats = self.get_loan_stats(start_date, end_date)
            fine_stats = self.get_fine_stats(start_date, end_date)
            book_stats = self.get_book_stats(start_date, end_date)
            event_stats = self.get_event_stats(start_date, end_date)

            stats = self.combine_stats(loan_stats, fine_stats, book_stats, event_stats)
            audit_log_entry = self.create_audit_log_entry(stats, start_date)
            self.insert_audit_log_entry(audit_log_entry)

            return stats
        except Exception as e:
            raise Exception("Failed to generate monthly report: " + str(e))

    def calculate_start_date(self, p_year, p_month):
        return datetime(p_year, p_month, 1)

    def calculate_end_date(self, p_year, p_month):
        if p_month == 12:
            return datetime(p_year + 1, 1, 1) - timedelta(days=1)
        else:
            return datetime(p_year, p_month + 1, 1) - timedelta(days=1)

    def get_loan_stats(self, start_date, end_date):
        loan_repository = LoanRepository()
        return loan_repository.get_stats(start_date, end_date)

    def get_fine_stats(self, start_date, end_date):
        fine_repository = FineRepository()
        return fine_repository.get_stats(start_date, end_date)

    def get_book_stats(self, start_date, end_date):
        book_repository = BookRepository()
        return book_repository.get_stats(start_date, end_date)

    def get_event_stats(self, start_date, end_date):
        event_repository = EventRepository()
        return event_repository.get_stats(start_date, end_date)

    def combine_stats(self, loan_stats, fine_stats, book_stats, event_stats):
        return {
            'loan_stats': loan_stats,
            'fine_stats': fine_stats,
            'book_stats': book_stats,
            'event_stats': event_stats
        }

    def create_audit_log_entry(self, stats, start_date):
        return AuditLog(
            stats=stats,
            timestamp=datetime.now(),
            report_date=start_date
        )

    def insert_audit_log_entry(self, audit_log_entry):
        try:
            audit_log_entry.save()
        except Exception as e:
            raise Exception("Failed to insert audit log entry: " + str(e))