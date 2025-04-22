

from typing import Dict
from sqlalchemy import create_engine, Column, Integer, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///membership.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class MembershipData(Base):
    __tablename__ = 'membership_data'
    id = Column(Integer, primary_key=True)
    auto_renewal_status = Column(Boolean)
    payment_processing_result = Column(String)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'auto_renewal_status': self.auto_renewal_status,
            'payment_processing_result': self.payment_processing_result
        }

Base.metadata.create_all(engine)

class MembershipRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_membership_data(self, membership_id: int) -> Dict:
        membership_data = self.db_session.query(MembershipData).filter_by(id=membership_id).first()
        return membership_data.to_dict()