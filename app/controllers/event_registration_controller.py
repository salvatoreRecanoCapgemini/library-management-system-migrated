

from flask import request, jsonify
from app import db
from app.models import EventRegistration, LibraryEvent
from datetime import datetime
import logging

@app.route("/event-registration", methods=["POST"])
def event_registration():
    try:
        event_id = request.json["event_id"]
        patron_id = request.json["patron_id"]
        if not event_id or not patron_id:
            return jsonify({"error": "Invalid event_id or patron_id"}), 400"}), 400
        new_registration = EventRegistration(event_id, patron_id, datetime.now(), 'REGISTERED')
        db.session.add(new_registration)
        db.session.commit()
        event = LibraryEvent.query.get(event_id)
        if event:
            event.current_participants += 1
            db.session.commit()
        else:
            logging.error(f"Event with id {event_id} not found")
            return jsonify({"error": "Event not found"}), 404
        return jsonify({"message": "Patron registered successfully"})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 400