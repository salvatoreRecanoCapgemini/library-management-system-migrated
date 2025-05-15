

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    available_copies = db.Column(db.Integer)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))