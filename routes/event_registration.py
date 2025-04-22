

from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

event_registration_blueprint = Blueprint('event_registration', __name__)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_participants = db.Column(db.Integer, nullable=False)
    current_participants = db.Column(db.Integer, nullable=False, default=0)
    patrons = db.relationship('Patron', secondary='event_registration', backref=db.backref('events', lazy=True))

class Patron(db.Model):
    id = db.Column(db.Integer, primary_key=True)

event_registration_blueprint.route('/register', methods=['POST'])
def register_patron_for_event():
    try:
        data = request.get_json()
        patron_id = data.get('patron_id')
        event_id = data.get('event_id')

        patron = Patron.query.get(patron_id)
        event = Event.query.get(event_id)

        if patron in event.patrons:
            raise Exception('Patron is already registered for the event')

        max_participants = event.max_participants
        current_participants = event.current_participants

        if current_participants >= max_participants:
            raise Exception('Event is fully booked')

        event.patrons.append(patron)
        event.current_participants = current_participants + 1
        db.session.add(event)
        db.session.commit()

        db.session.commit()

        return jsonify({'message': 'Patron registered successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Error registering patron'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 400