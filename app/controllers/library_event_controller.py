

from flask import jsonify
from app.services.library_event_service import LibraryEventService
import logging
from datetime import datetime

class LibraryEventController:
    def __init__(self, library_event_service: LibraryEventService):
        self.library_event_service = library_event_service
        self.logger = logging.getLogger(__name__)

    def handle_cancel_event(self, event_id: int):
        """
        Handles the cancellation of a library event.

        Args:
            event_id (int): The ID of the event to be cancelled.

        Returns:
            A JSON response containing the result of the cancellation.
        """
        try:
            if not isinstance(event_id, int) or event_id <= 0:
                self.logger.error("Invalid event ID")
                return jsonify({'error': 'Invalid event ID'}), 400
            result = self.library_event_service.cancel_event(event_id)
            return jsonify({'result': result})
        except Exception as e:
            self.logger.error(f"Error cancelling event: {str(e)}")
            return jsonify({'error': 'Error cancelling event'}), 500

    def handle_reschedule_event(self, event_id: int, new_date: str):
        """
        Handles the rescheduling of a library event.

        Args:
            event_id (int): The ID of the event to be rescheduled.
            new_date (str): The new date of the event in the format YYYY-MM-DD.

        Returns:
            A JSON response containing the result of the rescheduling as a JSON response.
        """
        try:
            if not isinstance(event_id, int) or event_id <= 0:
                self.logger.error("Invalid event ID")
                return jsonify({'error': 'Invalid event ID'}), 400
            try:
                datetime.strptime(new_date, '%Y-%m-%d')
            except ValueError:
                self.logger.error("Invalid date format")
                return jsonify({'error': 'Invalid date format'}), 400
            result = self.library_event_service.reschedule_event(event_id, new_date)
            return jsonify({'result': result})
        except Exception as e:
            self.logger.error(f"Error rescheduling event: {str(e)}")
            return jsonify({'error': 'Error rescheduling event'}), 500