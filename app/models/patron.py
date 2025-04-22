

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///patron.db')
Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patrons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    birth_date = Column(Date)
    membership_date = Column(Date)
    status = Column(String)

    def __init__(self, id, first_name, last_name, email, phone, birth_date, membership_date, status):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.membership_date = membership_date
        self.status = status

    def __repr__(self):
        return f'Patron(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, phone={self.phone}, birth_date={self.birth_date}, membership_date={self.membership_date}, status={self.status})'

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()