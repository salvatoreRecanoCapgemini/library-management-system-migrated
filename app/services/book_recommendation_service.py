

from sqlalchemy import func, desc, create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from app import db
from app.models import Loan, BookReview, Patron, Book

def generate_book_recommendations(patron_id):
    if not patron_id:
        raise ValueError("Patron ID is required")

    patron_reading_history = db.query(Loan).filter(Loan.patron_id == patron_id).filter(Loan.loan_date >= datetime.now() - timedelta(days=365)).all()
    patron_preferences = db.query(BookReview).filter(BookReview.patron_id == patron_id).all()
    patron_average_ratings = db.query(func.avg(BookReview.rating).label('average_rating'), Book.category, Book.author).filter(BookReview.book_id == Book.id).filter(BookReview.patron_id == patron_id).group_by(Book.category, Book.author).all()
    similar_patrons = db.query(Patron).filter(Patron.id != patron_id).filter(Patron.loans.any(Loan.book_id.in_([loan.book_id for loan in patron_reading_history]))).all()

    book_scores = []
    for book in db.query(Book).all():
        score = 0
        for rating in patron_average_ratings:
            if rating[1] == book.category:
                score += rating[0]
            if rating[2] == book.author:
                score += rating[0]
        if book.id in [loan.book_id for loan in patron_reading_history]:
            score += 1
        book_scores.append((book.id, book.title, score))

    # Insert the top 10 books with the highest score into a temporary table
    temp_table = db.Table('temp_table', db.metadata, 
        Column('book_id', Integer), 
        Column('title', String), 
        Column('score', Float)
    )
    db.metadata.create_all()
    db.session.execute(temp_table.insert(), book_scores)

    recommended_books = db.session.query(temp_table).order_by(desc(temp_table.c.score)).limit(10).all()

    return [{'book_id': book[0], 'title': book[1], 'score': book[2]} for book in recommended_books]