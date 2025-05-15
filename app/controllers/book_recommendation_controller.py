

from app.services.book_recommendation_system import BookRecommendationSystem

class BookRecommendationController:
    def __init__(self, db_connection):
        self.book_recommendation_system = BookRecommendationSystem(db_connection)

    def get_book_recommendations(self, patron_id):
        recommended_books = self.book_recommendation_system.generate_book_recommendations(patron_id)
        return recommended_books