

from app.services.book_review_service import BookReviewService

class BookReviewController:
    def add_book_review(self, book_id, patron_id, rating, review_text):
        book_review_service = BookReviewService()
        result = book_review_service.add_book_review(book_id, patron_id, rating, review_text)
        return result