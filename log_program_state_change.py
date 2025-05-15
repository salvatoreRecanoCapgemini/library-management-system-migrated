

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from enum import Enum as PyEnum

db = SQLAlchemy()

class ProgramStatus(PyEnum):
    PUBLISHED = 'published'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class Program(db.Model):
    id = Column(Integer, primary_key=True)
    status = Column(Enum(ProgramStatus), default=ProgramStatus.PUBLISHED)
    registrations = relationship('Registration', backref='program', lazy=True)

class Registration(db.Model):
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('program.id'))
    attendance = relationship('Attendance', backref='registration', lazy=True)
    completed = Column(Boolean, default=False)

class Attendance(db.Model):
    id = Column(Integer, primary_key=True)
    registration_id = Column(Integer, ForeignKey('registration.id'))
    attended = Column(Boolean, default=False)

def log_program_state_change(program_id, action, params):
    program = Program.query.get(program_id)
    if action == 'START_PROGRAM':
        start_program(program)
    elif action == 'RECORD_ATTENDANCE':
        record_attendance(program, params)
    elif action == 'COMPLETE_PROGRAM':
        complete_program(program)
    else:
        raise ValueError('Invalid action')

def start_program(program):
    if program.status != ProgramStatus.PUBLISHED:
        raise ValueError('Program is not in published status')
    if len(program.registrations) < 1:
        raise ValueError('Program has no registrations')
    # Initialize the session schedule
    program.status = ProgramStatus.IN_PROGRESS
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def record_attendance(program, params):
    if program.status != ProgramStatus.IN_PROGRESS:
        raise ValueError('Program is not in progress')
    if 'registration_id' not in params or 'attended' not in params:
        raise ValueError('Invalid params')
    attendance_records = Attendance.query.filter_by(registration_id=params['registration_id']).all()
    for record in attendance_records:
        record.attended = params['attended']
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    # Generate an attendance notification for each registration
    for record in attendance_records:
        # Send notification to record.registration.program_id

def complete_program(program):
    if program.status != ProgramStatus.IN_PROGRESS:
        raise ValueError('Program is not in progress')
    # Calculate completion statistics
    program.status = ProgramStatus.COMPLETED
    for registration in program.registrations:
        registration.completed = True
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    # Update completion status for participants