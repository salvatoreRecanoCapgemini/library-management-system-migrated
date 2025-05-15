

package models

class Book:
    """
    Represents a book with its attributes.

    Attributes:
        book_id (int): Unique identifier for the book.
        title (str): Title of the book.
        category (str): Category of the book.
        author (str): Author of the book.
        available_copies (int): Number of available copies of the book.
    """

    def __init__(self, book_id, title, category, author, available_copies):
        """
        Initializes a Book object.

        Args:
            book_id (int): Unique identifier for the book.
            title (str): Title of the book.
            category (str): Category of the book.
            author (str): Author of the book.
            available_copies (int): Number of available copies of the book.

        Raises:
            TypeError: If any of the input parameters are of the wrong type.
            ValueError: If any of the input parameters are invalid.
        """
        if not isinstance(book_id, int) or book_id <= 0:
            raise ValueError("Book ID must be a positive integer")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category must be a non-empty string")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Author must be a non-empty string")
        if not isinstance(available_copies, int) or available_copies < 0:
            raise ValueError("Available copies must be a non-negative integer")

        self.book_id = book_id
        self.title = title
        self.category = category
        self.author = author
        self.available_copies = available_copies