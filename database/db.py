

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db_connection(username, password, host, port, database):
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session