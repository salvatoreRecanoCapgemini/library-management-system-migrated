

from app.services.book_service import process_book_return

def handle_book_return_request(loan_id):
    if not isinstance(loan_id, int) or loan_id <= 0:
        raise ValueError("Invalid loan ID")
    process_book_return(loan_id)
    return {'message': 'Book returned successfully'}