

import sqlite3
from datetime import datetime, timedelta

class TemporaryTableService:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_temporary_table(self):
        self.cursor.execute('''
            CREATE TEMPORARY TABLE IF NOT EXISTS expiring_memberships (
                membership_id INTEGER,
                patron_id INTEGER,
                plan_id INTEGER,
                end_date DATE,
                auto_renewal BOOLEAN,
                status STRING
            )
        ''')

    def insert_into_temporary_table(self):
        try:
            self.cursor.execute('''
                INSERT INTO expiring_memberships (membership_id, patron_id, plan_id, end_date, auto_renewal, status)
                SELECT membership_id, patron_id, plan_id, end_date, auto_renewal, status
                FROM memberships
                WHERE end_date <= ?
            ''', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                print("The 'memberships' table does not exist.")
            else:
                print(f"An error occurred: {e}")

    def drop_temporary_table(self):
        try:
            self.cursor.execute('DROP TABLE expiring_memberships')
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(f"An error occurred: {e}")

    def close_connection(self):
        self.conn.close()