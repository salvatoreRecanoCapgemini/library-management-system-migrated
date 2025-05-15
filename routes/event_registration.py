

from flask import request, jsonify
from models import EventRegistration, LibraryEvent
from app import db
from datetime import datetime

@app.route('/register_for_event', methods=['POST'])
def register_for_event():
    try:
        event_id = request.json['event_id']
        patron_id = request.json['patron_id']
        if not event_id or not patron_id:
            return jsonify({'message': 'Invalid event_id or patron_id'}), 400
        new_registration = EventRegistration(event_id=event_id, patron_id=patron_id, registration_date=datetime.now(), attendance_status='REGISTERED')
        db.session.add(new_registration)
        db.session.commit()
        event = LibraryEvent.query.get(event_id)
        if event:
            event.current_participants += 1
            db.session.commit()
        else:
            return jsonify({'message': 'Event not found'}), 404
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error occurred during registration'}), 500