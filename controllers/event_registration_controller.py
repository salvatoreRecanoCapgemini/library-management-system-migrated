

from typing import Dict
from repositories import EventRepository, PatronRepository

class EventRegistrationController:
    def __init__(self, event_repository: EventRepository, patron_repository: PatronRepository):
        self.event_repository = event_repository
        self.patron_repository = patron_repository

    def handle_event_registration_request(self, event_id: int, patron_id: int) -> bool:
        if not isinstance(event_id, int) or not isinstance(patron_id, int):
            raise ValueError("Event ID and Patron ID must be integers")

        try:
            patron_registration_status = self.patron_repository.get_registration_status(patron_id)
            if not patron_registration_status:
                raise Exception("Patron is not registered")

            event_capacity_info = self.event_repository.get_event_capacity(event_id)
            if not event_capacity_info:
                raise Exception("Event capacity information not found")

            if event_capacity_info['current_capacity'] >= event_capacity_info['max_capacity']:
                raise Exception("Event is fully booked")

            self.patron_repository.register_patron_for_event(patron_id, event_id)
            return True
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def get_event_capacity(self, event_id: int) -> Dict:
        return self.event_repository.get_event_capacity(event_id)

    def get_registration_status(self, patron_id: int) -> bool:
        return self.patron_repository.get_registration_status(patron_id)

    def register_patron_for_event(self, patron_id: int, event_id: int) -> None:
        self.patron_repository.register_patron_for_event(patron_id, event_id)