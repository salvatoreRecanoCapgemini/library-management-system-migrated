

from flask import request, jsonify
from app.services.event_registration_service import EventRegistrationService

class EventRegistrationController:
    def register_for_event(self):
        try:
            event_id = int(request.args.get('event_id'))
            patron_id = int(request.args.get('patron_id'))
            if event_id and patron_id:
                EventRegistrationService().register_for_event(event_id, patron_id)
                return jsonify({'message': 'Registration successful'}), 200
            else:
                return jsonify({'message': 'Invalid input parameters'}), 400
        except ValueError:
            return jsonify({'message': 'Invalid input parameters'}), 400
        except Exception as e:
            return jsonify({'message': 'Internal server error'}), 500