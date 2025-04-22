

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book
import sqlalchemy

def update_book_availability(book_id, change):
    if not isinstance(book_id, int) or not isinstance(change, int):
        raise ValueError("Invalid input type")

    try:
        engine = create_engine('postgresql://user:password@host:port/dbname')
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            book = session.query(Book).filter_by(book_id=book_id).first()
            if book:
                book.available_copies += change
                session.commit()
            else:
                raise ValueError("Book not found")
        except sqlalchemy.exc.SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
    except sqlalchemy.exc.OperationalError as e:
        raise e