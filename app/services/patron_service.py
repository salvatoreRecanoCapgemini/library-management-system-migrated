

from app.models import Patron, db

class PatronService:
    def create_patron(self, first_name, last_name, email, phone, birth_date):
        patron = Patron(first_name=first_name, last_name=last_name, email=email, phone=phone, birth_date=birth_date)
        db.session.add(patron)
        db.session.commit()