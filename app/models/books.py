

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, DatabaseError
from datetime import datetime

db = SQLAlchemy()

class BookModel(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, publication_date, available_copies):
        self.title = title
        self.author = author
        self.publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
        self.available_copies = available_copies

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError('Book with this title already exists')
        except DatabaseError as e:
            db.session.rollback()
            raise ValueError('Database error: {}'.format(e))

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except DatabaseError as e:
            db.session.rollback()
            raise ValueError('Database error: {}'.format(e))

    def update_in_db(self, title, author, publication_date, available_copies):
        try:
            self.title = title
            self.author = author
            self.publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
            self.available_copies = available_copies
            db.session.commit()
        except DatabaseError as e:
            db.session.rollback()
            raise ValueError('Database error: {}'.format(e))

    @classmethod
    def find_by_title(cls, title):
        return BookModel.query.filter_by(title=title).first()

    @classmethod
    def find_by_author(cls, author):
        return cls.query.filter_by(author=author).first()

    @classmethod
    def find_by_publication_date(cls, publication_date):
        return cls.query.filter_by(publication_date=publication_date).first()

    @classmethod
    def find_by_available_copies(cls, available_copies):
        return cls.query.filter_by(available_copies=available_copies).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()