

from sqlalchemy import Column, Integer, String, Date, DECIMAL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publication_date = Column(Date)
    available_copies = Column(Integer)
    total_copies = Column(Integer)
    average_rating = Column(DECIMAL)

    def __init__(self, book_id, title, author, publication_date, available_copies, total_copies, average_rating):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.available_copies = available_copies
        self.total_copies = total_copies
        self.average_rating = average_rating

    @classmethod
    def get_books(cls, session, date_range):
        if not isinstance(date_range, tuple) or len(date_range) != 2:
            raise ValueError("date_range must be a tuple of two dates")
        start_date, end_date = date_range
        if not isinstance(start_date, Date) or not isinstance(end_date, Date):
            raise ValueError("start_date and end_date must be of type Date")
        try:
            return session.query(cls).filter(cls.publication_date.between(start_date, end_date)).all()
        except Exception as e:
            raise Exception("Error retrieving books from database: " + str(e))

def create_session():
    engine = create_engine('sqlite:///books.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()