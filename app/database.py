

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base = declarative_base()

class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer)
    attendance_log = Column(String)
    payment_status = Column(String)
    cost = Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db = Session()

def query_database(program_id):
    if not isinstance(program_id, int) or program_id <= 0:
        raise ValueError("Invalid program_id")

    try:
        metrics = {}
        metrics['total_registrations'] = get_total_registrations(program_id)
        metrics['total_attendees'] = get_total_attendees(program_id)
        metrics['total_revenue'] = get_total_revenue(program_id)
        metrics['average_attendance_rate'] = get_average_attendance_rate(program_id)
        return metrics
    except Exception as e:
        db.rollback()
        raise e

def get_total_registrations(program_id):
    return db.query(Registration).filter_by(program_id=program_id).count()

def get_total_attendees(program_id):
    return db.query(Registration).filter_by(program_id=program_id, attendance_log='ATTENDED').count()

def get_total_revenue(program_id):
    return db.query(Registration).filter_by(program_id=program_id, payment_status='PAID').with_entities(Registration.cost).all()

def get_average_attendance_rate(program_id):
    total_registrations = get_total_registrations(program_id)
    total_attendees = get_total_attendees(program_id)
    if total_registrations == 0:
        return 0
    return (total_attendees / total_registrations) * 100