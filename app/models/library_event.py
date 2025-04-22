

from datetime import date

class LibraryEvent:
    def __init__(self, event_id, title, event_date, status):
        if not isinstance(event_id, int):
            raise TypeError("event_id must be an integer")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not isinstance(event_date, date):
            raise TypeError("event_date must be a date")
        if not isinstance(status, str):
            raise TypeError("status must be a string")
        self.event_id = event_id
        self.title = title
        self.event_date = event_date
        self.status = status