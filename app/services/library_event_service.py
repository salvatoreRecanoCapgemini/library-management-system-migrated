

package app.services

import datetime
import logging
from app.models import Event, Patron, Registrant
from app.notifications import send_notification

class LibraryEventService:
    def __init__(self, db_session):
        self.db_session = db_session

    def cancel_event(self, event_id, event_data):
        if not self.event_exists(event_id):
            raise ValueError('Event does not exist')
        if self.get_event_status(event_id) == 'CANCELLED':
            raise ValueError('Event is already cancelled')
        affected_registrants = self.create_temp_table('affected_registrants', 'event_id', 'patron_id', event_id)
        self.update_event_status(event_id, 'CANCELLED')
        self.update_attendance_status(affected_registrants, 'NO_SHOW')
        self.process_notifications(affected_registrants)

    def reschedule_event(self, event_id, event_data):
        if not self.event_exists(event_id):
            raise ValueError('Event does not exist')
        self.validate_new_date(event_data)
        if self.get_event_date(event_id) == datetime.datetime.strptime(event_data['new_date'], '%Y-%m-%d').date():
            raise ValueError('New date is the same as the current date')
        schedule_conflicts = self.create_temp_table('schedule_conflicts', 'event_id', 'patron_id', event_id)
        self.update_event_date(event_id, event_data)
        self.notify_patrons(schedule_conflicts)

    def create_temp_table(self, table_name, event_id_column, patron_id_column, event_id):
        temp_table = []
        registrants = self.db_session.query(Registrant).filter_by(event_id=event_id).all()
        for registrant in registrants:
            temp_table.append({'event_id': event_id, 'patron_id': registrant.patron_id})
        return temp_table

    def update_event_status(self, event_id, status):
        try:
            event = self.db_session.query(Event).filter_by(id=event_id).first()
            event.status = status
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def update_attendance_status(self, registrants, status):
        for registrant in registrants:
            try:
                patron = self.db_session.query(Patron).filter_by(id=registrant['patron_id']).first()
                patron.attendance_status = status
                self.db_session.commit()
            except Exception as e:
                self.db_session.rollback()
                raise e

    def process_notifications(self, registrants):
        for registrant in registrants:
            try:
                patron = self.db_session.query(Patron).filter_by(id=registrant['patron_id']).first()
                if patron:
                    send_notification(patron.email, 'Event Cancellation', 'Your event has been cancelled.')
                else:
                    raise ValueError('Patron does not exist')
            except Exception as e:
                raise e

    def validate_new_date(self, event_data):
        new_date = datetime.datetime.strptime(event_data['new_date'], '%Y-%m-%d').date()
        if datetime.date.today() > new_date:
            raise ValueError('New date must be in the future')

    def update_event_date(self, event_id, event_data):
        try:
            event = self.db_session.query(Event).filter_by(id=event_id).first()
            event.date = datetime.datetime.strptime(event_data['new_date'], '%Y-%m-%d').date()
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def notify_patrons(self, schedule_conflicts):
        for conflict in schedule_conflicts:
            try:
                patron = self.db_session.query(Patron).filter_by(id=conflict['patron_id']).first()
                if patron:
                    send_notification(patron.email, 'Schedule Conflict', 'Your event has been rescheduled.'
                else:
                    raise ValueError('Patron does not exist')
            except Exception as e:
                raise e

    def event_exists(self, event_id):
        return self.db_session.query(Event).filter_by(id=event_id).first() is not None

    def get_event_status(self, event_id):
        event = self.db_session.query(Event).filter_by(id=event_id).first()
        return event.status if event else None

    def get_event_date(self, event_id):
        event = self.db_session.query(Event).filter_by(id=event_id).first()
        return event.date if event else None