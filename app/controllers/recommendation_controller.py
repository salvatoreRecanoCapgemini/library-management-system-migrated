

from flask import jsonify
from app.services.recommendation_service import RecommendationService

class RecommendationController:
    def get_recommendations(self, patron_id):
        if not patron_id:
            return jsonify({"error": "Patron ID is required"}), 400
        try:
            recommended_books = RecommendationService.generate_book_recommendations(patron_id)
            if recommended_books is None:
                return jsonify({"error": "No book recommendations found"}), 404
            return jsonify(recommended_books)
        except Exception as e:
            return jsonify({"error": "An error occurred while generating book recommendations"}), 500