

from sqlalchemy import Column, String, Date, Enum, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    patron_id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    membership_date = Column(Date, nullable=False, default=date.today)
    status = Column(Enum('ACTIVE', 'INACTIVE', name='status'), nullable=False, default='ACTIVE')
    birth_date = Column(Date, nullable=False, default=date(1900, 1, 1))
    reading_history = relationship("Book", secondary="patron_reading_history", backref="patrons")
    preferences = relationship("BookCategory", secondary="patron_preferences", backref="patrons")

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    categories = relationship("BookCategory", secondary="book_categories", backref="books")

class PatronReadingHistory(Base):
    __tablename__ = 'patron_reading_history'
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)

class BookCategory(Base):
    __tablename__ = 'book_categories'
    category_id = Column(Integer, primary_key=True)

class PatronPreferences(Base):
    __tablename__ = 'patron_preferences'
    patron_id = Column(Integer, ForeignKey('patrons.patron_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('book_categories.category_id'), primary_key=True)

class BookCategories(Base):
    __tablename__ = 'book_categories'
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('book_categories.category_id'), primary_key=True)