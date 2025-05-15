

from datetime import datetime
from typing import List, Dict
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dateutil.parser import parse

engine = create_engine('sqlite:///statistics.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class Fine(Base):
    __tablename__ = 'fines'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

Base.metadata.create_all(engine)

class StatisticsRepository:
    def __init__(self):
        self.session = Session()

    def _validate_dates(self, start_date: str, end_date: str) -> (datetime, datetime):
        try:
            start_date = parse(start_date)
            end_date = parse(end_date)
            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")
            return start_date, end_date
        except ValueError as e:
            raise ValueError("Invalid date format") from e

    def _execute_query(self, query):
        try:
            return query.all()
        except SQLAlchemyError as e:
            raise RuntimeError("Failed to execute query") from e

    def get_loan_stats(self, start_date: str, end_date: str) -> List[Dict]:
        start_date, end_date = self._validate_dates(start_date, end_date)
        query = self.session.query(Loan).filter(Loan.start_date >= start_date, Loan.end_date <= end_date)
        return self._execute_query(query)

    def get_fine_stats(self, start_date: str, end_date: str) -> List[Dict]:
        start_date, end_date = self._validate_dates(start_date, end_date)
        query = self.session.query(Fine).filter(Fine.start_date >= start_date, Fine.end_date <= end_date)
        return self._execute_query(query)

    def get_book_stats(self, start_date: str, end_date: str) -> List[Dict]:
        start_date, end_date = self._validate_dates(start_date, end_date)
        query = self.session.query(Book).filter(Book.start_date >= start_date, Book.end_date <= end_date)
        return self._execute_query(query)

    def get_event_stats(self, start_date: str, end_date: str) -> List[Dict]:
        start_date, end_date = self._validate_dates(start_date, end_date)
        query = self.session.query(Event).filter(Event.start_date >= start_date, Event.end_date <= end_date)
        return self._execute_query(query)