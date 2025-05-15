

from sqlalchemy import create_engine, sessionmaker, Column, Integer, String, DateTime, Enum, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    status = Column(Enum('ACTIVE', 'CANCELLED', 'RESCHEDULED'))
    date = Column(DateTime)
    registrations = relationship('Registration', backref='event')

class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    attendance_status = Column(Enum('ATTENDING', 'NO_SHOW'))

def manage_library_events(action, event_id, event_data):
    engine = create_engine('postgresql://user:password@host:port/dbname')
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()

    if action == 'CANCEL_EVENT':
        event = session.query(Event).get(event_id)
        if event:
            # Create a temporary table for affected registrants
            affected_registrants_table = Table('affected_registrants', metadata,
                Column('id', Integer, primary_key=True),
                Column('event_id', Integer),
                Column('attendance_status', Enum('ATTENDING', 'NO_SHOW'))
            )
            affected_registrants_table.create(engine, checkfirst=True)
            affected_registrants = session.query(Registration).filter_by(event_id=event_id).all()
            for registration in affected_registrants:
                session.execute(affected_registrants_table.insert().values(id=registration.id, event_id=registration.event_id, attendance_status=registration.attendance_status))
            # Update the event status to 'CANCELLED'
            event.status = 'CANCELLED'
            # Update the attendance status of affected registrations to 'NO_SHOW'
            for registration in affected_registrants:
                registration.attendance_status = 'NO_SHOW'
            # Process notifications for affected registrants
            for registrant in affected_registrants:
                # Send notification to registrant
                send_notification(registrant, 'Event Cancellation')
        else:
            raise ValueError('Event not found')

    elif action == 'RESCHEDULE_EVENT':
        event = session.query(Event).get(event_id)
        if event:
            # Validate the new date
            if 'new_date' in event_data and event_data['new_date'] > datetime.now():
                # Create a temporary table for conflict checking
                conflict_registrants_table = Table('conflict_registrants', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('event_id', Integer)
                )
                conflict_registrants_table.create(engine, checkfirst=True)
                conflict_registrants = session.query(Registration).filter_by(event_id=event_id).all()
                for registration in conflict_registrants:
                    session.execute(conflict_registrants_table.insert().values(id=registration.id, event_id=registration.event_id))
                # Update the event date
                event.date = event_data['new_date']
                # Notify affected patrons of scheduling conflicts
                for registrant in conflict_registrants:
                    # Send notification to registrant
                    send_notification(registrant, 'Event Reschedule')
            else:
                raise ValueError('Invalid new date')
        else:
            raise ValueError('Event not found')

    else:
        raise ValueError('Invalid action')

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise e

def send_notification(registrant, subject):
    msg = MIMEMultipart()
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'recipient-email@gmail.com'
    msg['Subject'] = subject
    body = 'Please check the new event schedule.'
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], 'your-password')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()