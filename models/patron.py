

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patron.db'
db = SQLAlchemy(app)

class Patron(db.Model):
    __tablename__ = 'patrons'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(Date, nullable=False)
    membership_date = db.Column(Date, default=func.current_date())
    status = db.Column(db.String(10), default='ACTIVE', nullable=False)

    registrations = db.relationship('Registration', backref='patron')

    def __init__(self, first_name, last_name, email, phone, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date

    def __repr__(self):
        return f"Patron('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone}', '{self.birth_date}')"

class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.id'), nullable=False)

    def __init__(self, patron_id):
        self.patron_id = patron_id

    def __repr__(self):
        return f"Registration('{self.patron_id}')"