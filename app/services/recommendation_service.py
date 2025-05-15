

from typing import List, Dict
from app.models import Patron, Book
from app.repositories import PatronRepository, BookRepository

class RecommendationService:
    def __init__(self, patron_repository: PatronRepository, book_repository: BookRepository):
        self.patron_repository = patron_repository
        self.book_repository = book_repository

    def generate_book_recommendations(self, patron_id: int) -> List[Dict]:
        try:
            if not isinstance(patron_id, int) or patron_id <= 0:
                raise ValueError("Invalid patron ID")
            patron = self.patron_repository.get_patron(patron_id)
            if not patron:
                raise ValueError("Patron not found")
            reading_history = patron.reading_history
            preferences = patron.preferences
            if not reading_history or not preferences:
                return []
            recommended_books = []
            for book in self.book_repository.get_books():
                score = self.calculate_score(book, reading_history, preferences)
                recommended_books.append({'book_id': book.book_id, 'title': book.title, 'score': score})
            recommended_books.sort(key=lambda x: x['score'], reverse=True)
            recommended_books = recommended_books[:10]
            return recommended_books
        except Exception as e:
            raise Exception("Failed to generate book recommendations") from e

    def calculate_score(self, book: Book, reading_history: List[Book], preferences: Dict) -> float:
        score = 0
        if book in reading_history:
            score += 1
        if book.genre in preferences:
            score += preferences[book.genre]
        return score