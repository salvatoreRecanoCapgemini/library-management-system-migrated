

from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publication_date = Column(Date)
    available_copies = Column(Integer)

    __table_args__ = (CheckConstraint('available_copies >= 0', name='check_available_copies'),)

    loans = relationship('Loan', backref='book')

    def __init__(self, title, author, publication_date, available_copies):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.available_copies = available_copies

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.publication_date}', {self.available_copies})"