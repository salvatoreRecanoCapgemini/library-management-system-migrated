

package app.services

import app.models.Patron
import app.models.Book
import app.repositories.PatronRepository
import app.repositories.BookRepository

class RecommendationService:
    def __init__(self, patron_repository, book_repository):
        self.patron_repository = patron_repository
        self.book_repository = book_repository

    def generate_recommendations(self, patron_id):
        try:
            patron = self.patron_repository.get_by_id(patron_id)
            if patron is None:
                return []
            reading_history = patron.reading_history
            preferences = patron.preferences

            books = self.book_repository.get_all()
            if not books:
                return []

            recommended_books = []
            for book in books:
                if book not in reading_history:
                    score = self.calculate_score(book, reading_history, preferences)
                    recommended_books.append((book, score))

            recommended_books.sort(key=lambda x: x[1], reverse=True)
            return [book[0] for book in recommended_books[:10]]
        except Exception as e:
            # handle exception
            return []

    def calculate_score(self, book, reading_history, preferences):
        score = 0
        if book.genres:
            for preference in preferences:
                score += 1
        if reading_history:
            for read_book in reading_history:
                if read_book.author == book.author:
                    score += 1
        return score