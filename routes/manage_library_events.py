

from flask import request, jsonify
from models import LibraryEvent, EventRegistration, Patron, AuditLog
from datetime import date
from db import db

@app.route('/manage_library_events', methods=['POST'])
def manage_library_events():
    data = request.json
    if not data or 'action' not in data or 'event_id' not in data or 'event_data' not in data:
        return jsonify({'error': 'Missing parameters'}), 400
    
    action = data['action']
    event_id = data['event_id']
    event_data = data['event_data']

    if action == 'CANCEL_EVENT':
        affected_registrants = EventRegistration.query.filter_by(event_id=event_id).all()
        if affected_registrants is None:
            return jsonify({'error': 'Event not found'}), 400
        library_event = LibraryEvent.query.get(event_id)
        library_event.status = 'CANCELLED'
        db.session.commit()
        for registrant in affected_registrants:
            registrant.attendance_status = 'NO_SHOW'
            db.session.commit()
            patron = Patron.query.get(registrant.patron_id)
            # Implement notification to patron

    elif action == 'RESCHEDULE_EVENT':
        if 'new_date' not in event_data:
            return jsonify({'error': 'Missing new date'}), 400
        new_date = event_data['new_date']
        if new_date < date.today():
            return jsonify({'error': 'New date is in the past'}), 400
        schedule_conflicts = EventRegistration.query.filter_by(event_id=event_id).all()
        if schedule_conflicts is None:
            return jsonify({'error': 'Event not found'}), 400
        library_event = LibraryEvent.query.get(event_id)
        library_event.event_date = new_date
        db.session.commit()
        for registrant in schedule_conflicts:
            patron = Patron.query.get(registrant.patron_id)
            # Implement notification to patron

    else:
        return jsonify({'error': 'Invalid action'}), 400

    return jsonify({'message': 'Library event managed successfully'}), 200