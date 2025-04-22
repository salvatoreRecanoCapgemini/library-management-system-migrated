

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Patron, Book, Loan, BookReview

Base = declarative_base()

class BookRecommendationSystem:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.session_maker = sessionmaker(bind=self.engine)

    def generate_book_recommendations(self, patron_id):
        if not isinstance(patron_id, int) or patron_id <= 0:
            raise ValueError("Invalid patron_id")

        session = self.session_maker()
        try:
            patron = session.query(Patron).filter(Patron.id == patron_id).first()
            if patron is None:
                raise ValueError("Patron not found")

            reading_history = session.query(Loan).filter(Loan.patron_id == patron_id).all()
            preferences = session.query(BookReview).filter(BookReview.patron_id == patron_id).all()

            ratings = {}
            for review in preferences:
                ratings[review.book_id] = review.rating

            similar_patrons = session.query(Patron).filter(Patron.id != patron_id).all()

            scores = {}
            for book in session.query(Book).all():
                score = 0
                for loan in reading_history:
                    if loan.book_id == book.id:
                        score += 1
                for review in preferences:
                    if review.book_id == book.id:
                        score += review.rating
                for similar_patron in similar_patrons:
                    similar_loans = session.query(Loan).filter(Loan.patron_id == similar_patron.id).all()
                    for similar_loan in similar_loans:
                        if similar_loan.book_id == book.id:
                            score += 1
                scores[book.id] = score

            recommended_books = []
            for book_id, score in scores.items():
                if score > 0:
                    recommended_books.append((book_id, score))

            existing_recommended_books = session.query(Book).filter(Book.id.in_(recommended_books)).all()
            for book in existing_recommended_books:
                recommended_books.remove((book.id, scores[book.id]))

            session.execute("INSERT INTO recommended_books (book_id, score) VALUES (:book_id, :score)", recommended_books)

            return session.query(Book).filter(Book.id.in_([book[0] for book in recommended_books])).all()
        except Exception as e:
            print(f'Error: {e}')
        finally:
            session.close()