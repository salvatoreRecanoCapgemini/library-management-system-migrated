

from dataclasses import dataclass
from typing import Dict
import logging

@dataclass
class Notification:
    patron_id: int
    email: str
    message: str

    def __post_init__(self):
        if not isinstance(self.patron_id, int) or self.patron_id <= 0:
            raise ValueError("Patron ID must be a positive integer")
        if not isinstance(self.email, str) or not self.email:
            raise ValueError("Email must be a non-empty string")
        if not isinstance(self.message, str) or not self.message:
            raise ValueError("Message must be a non-empty string")

    def construct_notification_message(self) -> str:
        return f"Notification for patron {self.patron_id}: {self.message}"

    def store_in_temporary_storage(self, storage: Dict[int, str]) -> None:
        try:
            storage[self.patron_id] = self.construct_notification_message()
        except Exception as e:
            logging.error(f"Failed to store notification in temporary storage: {e}")

def test_notification():
    notification = Notification(1, "test@example.com", "Test message")
    storage = {}
    notification.store_in_temporary_storage(storage)
    assert storage[1] == "Notification for patron 1: Test message"

def test_notification_validation():
    try:
        Notification(0, "test@example.com", "Test message")
        assert False, "Expected ValueError for invalid patron ID"
    except ValueError:
        pass

    try:
        Notification(1, "", "Test message")
        assert False, "Expected ValueError for invalid email"
    except ValueError:
        pass

    try:
        Notification(1, "test@example.com", "")
        assert False, "Expected ValueError for invalid message"
    except ValueError:
        pass