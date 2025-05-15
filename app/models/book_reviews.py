

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookReviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'), nullable=False)
    review_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Integer, nullable=False)