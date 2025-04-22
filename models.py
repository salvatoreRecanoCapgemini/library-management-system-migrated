

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Loans(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'))
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String)
    book = db.relationship('Books', backref=db.backref('loans', lazy=True))
    patron = db.relationship('Patrons', backref=db.backref('loans', lazy=True))

class Fines(db.Model):
    __tablename__ = 'fines'
    fine_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'))
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.loan_id'))
    amount = db.Column(db.Float)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String)
    patron = db.relationship('Patrons', backref=db.backref('fines', lazy=True))
    loan = db.relationship('Loans', backref=db.backref('fines', lazy=True))

class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    available_copies = db.Column(db.Integer)

class Patrons(db.Model):
    __tablename__ = 'patrons'
    patron_id = db.Column(db.Integer, primary_key=True)

Index('ix_loans_due_date', Loans.due_date)
Index('ix_fines_issue_date', Fines.issue_date)
Index('ix_fines_due_date', Fines.due_date)