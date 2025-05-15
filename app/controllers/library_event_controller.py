

from flask import Blueprint, request, jsonify
from app.models import LibraryEvent, Notification, Conflict
from app import db

library_event_controller = Blueprint('library_event_controller', __name__)

class LibraryEventController:
    def __init__(self, library_event_model, notification_model, conflict_model, db):
        self.library_event_model = library_event_model
        self.notification_model = notification_model
        self.conflict_model = conflict_model
        self.db = db

    def cancel_event(self):
        event_id = request.json['event_id']
        event = self.library_event_model.query.get(event_id)
        if event:
            event.status = 'cancelled'
            self.db.session.commit()
            return jsonify({'message': 'Event cancelled successfully'}), 200
        return jsonify({'message': 'Event not found'}), 404

    def reschedule_event(self):
        event_id = request.json['event_id']
        new_date = request.json['new_date']
        event = self.library_event_model.query.get(event_id)
        if event:
            event.date = new_date
            self.db.session.commit()
            return jsonify({'message': 'Event rescheduled successfully'}), 200
        return jsonify({'message': 'Event not found'}), 404

    def log_notifications_and_conflicts(self):
        notification_data = request.json['notification']
        conflict_data = request.json['conflict']
        notification = self.notification_model(**notification_data)
        conflict = self.conflict_model(**conflict_data)
        self.db.session.add(notification)
        self.db.session.add(conflict)
        self.db.session.commit()
        return jsonify({'message': 'Notification and conflict logged successfully'}), 200

library_event_controller.add_url_rule('/cancel_event', 'cancel_event', view_func=LibraryEventController(LibraryEvent, Notification, Conflict).cancel_event, methods=['POST'])
library_event_controller.add_url_rule('/reschedule_event', 'reschedule_event', view_func=LibraryEventController(LibraryEvent, Notification, Conflict).reschedule_event, methods=['POST'])
library_event_controller.add_url_rule('/log_notifications_and_conflicts', 'log_notifications_and_conflicts', view_func=LibraryEventController(LibraryEvent, Notification, Conflict).log_notifications_and_conflicts, methods=['POST'])