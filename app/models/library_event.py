

from datetime import date

class LibraryEvent:
    def __init__(self, event_id, title, event_date, status, max_participants, current_participants):
        if not isinstance(event_id, int):
            raise TypeError("event_id must be an integer")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not isinstance(event_date, date):
            raise TypeError("event_date must be a date")
        if not isinstance(status, str):
            raise TypeError("status must be a string")
        if not isinstance(max_participants, int):
            raise TypeError("max_participants must be an integer")
        if not isinstance(current_participants, int):
            raise TypeError("current_participants must be an integer")
        if current_participants > max_participants:
            raise ValueError("current_participants cannot be greater than max_participants")

        self.event_id = event_id
        self.title = title
        self.event_date = event_date
        self.status = status
        self.max_participants = max_participants
        self.current_participants = current_participants

    def __repr__(self):
        return f"LibraryEvent(event_id={self.event_id}, title='{self.title}', event_date={self.event_date}, status='{self.status}', max_participants={self.max_participants}, current_participants={self.current_participants})"