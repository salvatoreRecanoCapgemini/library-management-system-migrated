

from flask import Flask, request, jsonify
from models import LibraryEvent, EventRegistration, Patron, AuditLog
from datetime import datetime
import json

app = Flask(__name__)

def send_notification(registrant, message):
    # Implement notification logic here
    pass

def create_patron(first_name, last_name, email, phone, birth_date):
    patron = Patron(first_name=first_name, last_name=last_name, email=email, phone=phone, birth_date=birth_date)
    patron.save()
    return patron

@app.route('/manage_library_events', methods=['POST'])
def manage_library_events():
    action = request.json['action']
    event_id = request.json.get('event_id')
    event_data = request.json.get('event_data')

    if not event_id:
        return jsonify({'error': 'Event ID not provided'}), 400

    if action == 'CANCEL_EVENT':
        event = LibraryEvent.query.get(event_id)
        if event:
            event.status = 'CANCELLED'
            event.save()
            registrants = EventRegistration.query.filter_by(event_id=event_id).all()
            for registrant in registrants:
                registrant.status = 'CANCELLED'
                registrant.save()
                send_notification(registrant, 'Event cancelled')
                audit_log = AuditLog(event_id=event_id, action='CANCEL_EVENT')
                audit_log.save()
        else:
            return jsonify({'error': 'Event not found'}), 404
    elif action == 'RESCHEDULE_EVENT':
        event = LibraryEvent.query.get(event_id)
        if event:
            new_date = event_data.get('new_date')
            if not new_date:
                return jsonify({'error': 'New date not provided'}), 400
            try:
                new_date = datetime.strptime(new_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
            conflicts = LibraryEvent.query.filter_by(date=new_date).all()
            if conflicts:
                for conflict in conflicts:
                    registrants = EventRegistration.query.filter_by(event_id=conflict.id).all()
                    for registrant in registrants:
                        send_notification(registrant, 'Event rescheduled')
            event.date = new_date
            event.save()
            audit_log = AuditLog(event_id=event_id, action='RESCHEDULE_EVENT')
            audit_log.save()
        else:
            return jsonify({'error': 'Event not found'}), 404
    else:
        return jsonify({'error': 'Invalid action'}), 400

@app.route('/patrons', methods=['POST'])
def create_patron_route():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    phone = data['phone']
    birth_date = data['birth_date']
    create_patron(first_name, last_name, email, phone, birth_date)
    return 'Patron created successfully'