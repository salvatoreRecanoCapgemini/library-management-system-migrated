

package app.services

import sqlite3
from typing import List, Tuple

class BookRecommendationSystem:
    def __init__(self, db_connection: sqlite3.Connection):
        self.db_connection = db_connection
        self.cursor = self.db_connection.cursor()

    def generate_book_recommendations(self, patron_id: int) -> List[Tuple]:
        if not isinstance(patron_id, int) or patron_id <= 0:
            raise ValueError("Invalid patron ID")

        try:
            patron_history = self.cursor.execute('''
                SELECT DISTINCT category, author 
                FROM loans 
                JOIN books ON loan_id = book_id 
                WHERE patron_id = :patron_id AND loan_date >= CURRENT_DATE - INTERVAL '1 year'
            ''', {'patron_id': patron_id}).fetchall()

            patron_preferences = self.cursor.execute('''
                SELECT category, author 
                FROM book_reviews 
                JOIN books ON book_id = book_id 
                WHERE patron_id = :patron_id 
                GROUP BY category, author
            ''', {'patron_id': patron_id}).fetchall()

            similar_patrons = self.cursor.execute('''
                SELECT DISTINCT patron_id 
                FROM loans 
                JOIN loans ON book_id = book_id 
                WHERE patron_id = :patron_id AND patron_id != :patron_id
            ''', {'patron_id': patron_id}).fetchall()

            if not patron_history and not patron_preferences and not similar_patrons:
                return []

            categories = [category for category, _ in patron_history] if patron_history else []
            authors = [author for _, author in patron_preferences] if patron_preferences else []
            similar_patrons = [patron[0] for patron in similar_patrons] if similar_patrons else []

            recommended_books = self.cursor.execute('''
                SELECT book_id, title, 
                (CASE WHEN category IN (:categories) THEN 2 ELSE 0 END + 
                 CASE WHEN author IN (:authors) THEN 1.5 ELSE 0 END + 
                 COALESCE((SELECT avg_rating FROM patron_ratings WHERE category = category), 0) + 
                 (SELECT COUNT(*) FROM loans WHERE book_id = book_id AND patron_id IN (:similar_patrons)) * 0.1) as score 
                FROM books 
                WHERE book_id NOT IN (SELECT book_id FROM loans WHERE patron_id = :patron_id) AND available_copies > 0 
                ORDER BY score DESC LIMIT 10
            ''', {'patron_id': patron_id, 'categories': categories, 'authors': authors, 'similar_patrons': similar_patrons}).fetchall()

            return recommended_books

        except sqlite3.Error as e:
            self.db_connection.rollback()
            raise e