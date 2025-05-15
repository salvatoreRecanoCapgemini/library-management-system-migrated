

from app.models.book import Book
from sqlalchemy.exc import NoResultFound, IntegrityError
from app import db
import logging

class BookService:
    def update_availability(self, book_id, change_value):
        """
        Updates the availability of a book by the specified change value.

        Args:
            book_id (int): The ID of the book to update.
            change_value (int): The value to add to the available copies.

        Raises:
            NoResultFound: If the book with the specified ID is not found.
            ValueError: If the change value is not a valid integer.
            IntegrityError: If a database error occurs during commit.
        """
        if not isinstance(change_value, int):
            raise ValueError("Change value must be an integer")

        try:
            book = Book.query.get(book_id)
            if book:
                if change_value == 0:
                    logging.warning("Change value is zero, no update will be made")
                else:
                    book.available_copies += change_value
                    db.session.commit()
            else:
                raise NoResultFound('Book not found')
        except NoResultFound as e:
            raise e
        except IntegrityError as e:
            logging.error("Database error during commit: %s", e)
            raise e