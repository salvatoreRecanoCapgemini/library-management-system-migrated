

from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error

class StatisticsRepository:
    def __init__(self, db_name):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    def calculate_start_date(self, year, month):
        return datetime(year, month, 1)

    def calculate_end_date(self, year, month):
        if month == 12:
            return datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            return datetime(year, month + 1, 1) - timedelta(days=1)

    def get_loan_stats(self, start_date, end_date):
        query = """
            SELECT 
                COUNT(*) as total_loans,
                SUM(CASE WHEN due_date < ? THEN 1 ELSE 0 END) as overdue_loans,
                COUNT(DISTINCT borrower_id) as active_borrowers
            FROM loans
            WHERE loan_date BETWEEN ? AND ?
        """
        self.cursor.execute(query, (end_date, start_date, end_date))
        row = self.cursor.fetchone()
        return {
            'total_loans': row[0],
            'overdue_loans': row[1],
            'active_borrowers': row[2]
        }

    def get_fine_stats(self, start_date, end_date):
        query = """
            SELECT 
                SUM(amount) as total_fines,
                SUM(CASE WHEN paid THEN amount ELSE 0 END) as paid_fines,
                SUM(CASE WHEN NOT paid THEN amount ELSE 0 END) as pending_fines
            FROM fines
            WHERE fine_date BETWEEN ? AND ?
        """
        self.cursor.execute(query, (start_date, end_date))
        row = self.cursor.fetchone()
        return {
            'total_fines': row[0],
            'paid_fines': row[1],
            'pending_fines': row[2]
        }

    def get_book_stats(self, start_date, end_date):
        query = """
            SELECT 
                COUNT(*) as books_in_circulation,
                SUM(available_copies) as total_available_copies,
                AVG(rating) as average_rating
            FROM books
            WHERE last_borrowed BETWEEN ? AND ?
        """
        self.cursor.execute(query, (start_date, end_date))
        row = self.cursor.fetchone()
        return {
            'books_in_circulation': row[0],
            'total_available_copies': row[1],
            'average_rating': row[2]
        }

    def get_event_stats(self, start_date, end_date):
        query = """
            SELECT 
                COUNT(*) as total_events,
                SUM(participants) as total_participants,
                AVG(capacity_utilization) as average_capacity_utilization
            FROM events
            WHERE event_date BETWEEN ? AND ?
        """
        self.cursor.execute(query, (start_date, end_date))
        row = self.cursor.fetchone()
        return {
            'total_events': row[0],
            'total_participants': row[1],
            'average_capacity_utilization': row[2]
        }

    def combine_stats(self, loan_stats, fine_stats, book_stats, event_stats):
        return {
            'loan_stats': loan_stats,
            'fine_stats': fine_stats,
            'book_stats': book_stats,
            'event_stats': event_stats
        }

    def create_audit_log_entry(self, stats, start_date):
        return {
            'stats': stats,
            'timestamp': datetime.now()
        }

    def insert_audit_log_entry(self, audit_log_entry):
        query = """
            INSERT INTO audit_log (stats, timestamp)
            VALUES (?, ?)
        """
        self.cursor.execute(query, (str(audit_log_entry['stats']), audit_log_entry['timestamp']))
        self.conn.commit()

    def generate_monthly_statistics(self, year, month):
        if not (1 <= month <= 12):
            raise ValueError("Invalid month")
        if not (1 <= year <= 9999):
            raise ValueError("Invalid year")
        start_date = self.calculate_start_date(year, month)
        end_date = self.calculate_end_date(year, month)

        loan_stats = self.get_loan_stats(start_date, end_date)
        fine_stats = self.get_fine_stats(start_date, end_date)
        book_stats = self.get_book_stats(start_date, end_date)
        event_stats = self.get_event_stats(start_date, end_date)

        stats = self.combine_stats(loan_stats, fine_stats, book_stats, event_stats)

        audit_log_entry = self.create_audit_log_entry(stats, start_date)
        self.insert_audit_log_entry(audit_log_entry)

        return stats