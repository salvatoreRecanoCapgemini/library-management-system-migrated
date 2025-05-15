

from app import db

class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    status = db.Column(db.String(50))

    book = db.relationship('Book', backref=db.backref('reservations', lazy=True))

    def __init__(self, book_id, status):
        self.book_id = book_id
        self.status = status

    def __repr__(self):
        return f"Reservation('{self.reservation_id}', '{self.book_id}', '{self.status}')"

    def is_valid(self):
        if not self.book_id:
            return False
        if not self.status:
            return False
        return True