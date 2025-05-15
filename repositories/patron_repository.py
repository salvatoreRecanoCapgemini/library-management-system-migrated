

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import Optional

Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    active_loans = Column(Integer)

class PatronRepository:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def get_patron_by_id(self, patron_id: int) -> Optional[Patron]:
        try:
            patron = self.db_session.query(Patron).filter_by(id=patron_id).first()
            return patron
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def check_patron_status(self, patron_id: int) -> bool:
        if not isinstance(patron_id, int) or patron_id <= 0:
            raise ValueError("Invalid patron ID")
        patron = self.get_patron_by_id(patron_id)
        if patron is None:
            return False
        return patron.status == 'ACTIVE'

    def check_active_loans(self, patron_id: int) -> bool:
        if not isinstance(patron_id, int) or patron_id <= 0:
            raise ValueError("Invalid patron ID")
        patron = self.get_patron_by_id(patron_id)
        if patron is None:
            return False
        return patron.active_loans < 5

engine = create_engine('sqlite:///patron.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()