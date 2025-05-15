

from app.services.book_review_service import add_book_review

def add_book_review_controller(book_id, patron_id, rating, review_text):
    try:
        if not isinstance(book_id, int) or not isinstance(patron_id, int) or not isinstance(rating, int) or not isinstance(review_text, str):
            return {"error": "Invalid input parameters"}
        result = add_book_review(book_id, patron_id, rating, review_text)
        if result:
            return {"message": "Book review added successfully", "review_id": result}
        else:
            return {"error": "Failed to add book review"}
    except Exception as e:
        return {"error": str(e)}