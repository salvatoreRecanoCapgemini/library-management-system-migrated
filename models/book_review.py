

package models

class BookReview:
    def __init__(self, review_id: int, patron_id: int, book_id: int, rating: int):
        if not isinstance(review_id, int) or not isinstance(patron_id, int) or not isinstance(book_id, int) or not isinstance(rating, int):
            raise ValueError("Invalid input type")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.review_id = review_id
        self.patron_id = patron_id
        self.book_id = book_id
        self.rating = rating