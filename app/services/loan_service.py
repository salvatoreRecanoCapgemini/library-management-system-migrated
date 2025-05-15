

from datetime import datetime, timedelta
from app import db
from app.models import Loan, Reservation

def extend_loan_period(p_loan_id, p_extension_days=7):
    """
    Extend the loan period by updating the due date and incrementing the extension count.

    Args:
        p_loan_id (int): The ID of the loan to extend.
        p_extension_days (int, optional): The number of days to extend the loan. Defaults to 7.

    Raises:
        ValueError: If the active loan is not found, maximum extensions are reached, or the book has pending reservations.
        Exception: If an error occurs during database commit.
    """
    if not isinstance(p_extension_days:
        raise ValueError('Extension days must be a positive integer')
    loan = Loan.query.filter_by(id=p_loan_id, status='ACTIVE').first()
    if loan is None:
        raise ValueError('Active loan not found')
    if loan.extensions_count >= 2:
        raise ValueError('Maximum extensions reached')
    pending_reservations = Reservation.query.filter_by(book_id=loan.book_id, status='PENDING').all()
    if pending_reservations:
        raise ValueError('Book has pending reservations')
    loan.due_date += timedelta(days=p_extension_days)
    loan.extensions_count += 1
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception('Error extending loan period: {}'.format(str(e)))