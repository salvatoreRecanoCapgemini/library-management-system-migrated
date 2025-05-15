

import sqlite3
import logging

class NotificationRepository:
    def __init__(self, db_name):
        self.db_name = db_name
        self.log = logging.getLogger(__name__)

    def prepare_notification(self, loan_id, patron_id, fine_amount):
        try:
            if not patron_id:
                raise ValueError("Patron ID is required")

            query = "SELECT patrons.first_name, books.title FROM patrons INNER JOIN loans ON patrons.patron_id = loans.patron_id INNER JOIN books ON loans.book_id = books.book_id WHERE loans.loan_id = ? AND patrons.patron_id = ?"
            params = [loan_id, patron_id]
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            if not result:
                raise ValueError("No results found for the given loan ID and patron ID")

            patron_name = result[0]
            book_title = result[1]
            notification_message = f"Dear {patron_name}, your book '{book_title}' is overdue. Please pay the fine of ${fine_amount}."
            conn.close()
            return notification_message
        except Exception as e:
            self.log.error(f"An error occurred: {e}")
            if conn:
                conn.close()
            return None