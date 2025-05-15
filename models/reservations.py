

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Reservations(Base):
    __tablename__ = 'reservations'
    reservation_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'))
    status = Column(String)