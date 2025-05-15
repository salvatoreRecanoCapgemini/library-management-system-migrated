

from app import db

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    category = db.Column(db.String)
    author = db.Column(db.String)
    available_copies = db.Column(db.Integer)

    loans = db.relationship('Loan', backref='book', lazy=True)
    reservations = db.relationship('Reservation', backref='book', lazy=True)

    def __init__(self, book_id, title, category, author, available_copies):
        self.book_id = book_id
        self.title = title
        self.category = category
        self.author = author
        self.available_copies = available_copies

    def calculate_score(self, reading_history, preferences):
        if not isinstance(reading_history, dict) or not isinstance(preferences, dict):
            raise ValueError("Invalid input type")

        category_score = 0
        author_score = 0
        popularity_score = 0

        if self.category in reading_history:
            category_score = reading_history[self.category]
        if self.author in reading_history:
            author_score = reading_history[self.author]

        if self.loans:
            loan_count = len(self.loans)
        else:
            loan_count = 0

        if self.reservations:
            reservation_count = len(self.reservations)
        else:
            reservation_count = 0

        if loan_count + reservation_count > 0:
            popularity_score = (loan_count + reservation_count) / (loan_count + reservation_count + self.available_copies)

        score = category_score + author_score + popularity_score

        if self.category in preferences:
            score += preferences[self.category]
        if self.author in preferences:
            score += preferences[self.author]

        return score