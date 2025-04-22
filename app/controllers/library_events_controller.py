

package app.controllers

import (
	"database/sql"
	"errors"
	"fmt"
)

type LibraryEventsController struct {
	db *sql.DB
}

func NewLibraryEventsController(db *sql.DB) *LibraryEventsController {
	return &LibraryEventsController{db: db}
}

func (lec *LibraryEventsController) ManageLibraryEvents(action string, eventID int, eventData map[string]interface{}) error {
	if action != "CANCEL_EVENT" && action != "RESCHEDULE_EVENT" {
		return errors.New("invalid action")
	}

	switch action {
	case "CANCEL_EVENT":
		return lec.cancelEvent(eventID, eventData)
	case "RESCHEDULE_EVENT":
		return lec.rescheduleEvent(eventID, eventData)
	}

	return nil
}

func (lec *LibraryEventsController) cancelEvent(eventID int, eventData map[string]interface{}) error {
	// Create a temporary table of affected registrants
	_, err := lec.db.Exec("CREATE TEMPORARY TABLE affected_registrants (event_id INT, patron_id INT)")
	if err != nil {
		return err
	}

	// Update the event status to 'CANCELLED'
	_, err = lec.db.Exec("UPDATE events SET status = 'CANCELLED' WHERE id = ?", eventID)
	if err != nil {
		return err
	}

	// Update the attendance status of affected registrants to 'NO_SHOW'
	_, err = lec.db.Exec("UPDATE registrations SET attendance_status = 'NO_SHOW' WHERE event_id = ?", eventID)
	if err != nil {
		return err
	}

	// Process notifications for affected registrants
	err = lec.processNotifications("affected_registrants")
	if err != nil {
		return err
	}

	return nil
}

func (lec *LibraryEventsController) rescheduleEvent(eventID int, eventData map[string]interface{}) error {
	// Validate the new date
	if _, ok := eventData["new_date"]; !ok {
		return errors.New("new date is required")
	}

	// Create a temporary table of schedule conflicts
	_, err := lec.db.Exec("CREATE TEMPORARY TABLE schedule_conflicts (event_id INT, patron_id INT)")
	if err != nil {
		return err
	}

	// Update the event date
	_, err = lec.db.Exec("UPDATE events SET date = ? WHERE id = ?", eventData["new_date"], eventID)
	if err != nil {
		return err
	}

	// Notify affected patrons of schedule conflicts
	err = lec.notifyPatrons("schedule_conflicts")
	if err != nil {
		return err
	}

	return nil
}

func (lec *LibraryEventsController) processNotifications(tempTable string) error {
	// Process notifications for affected registrants
	_, err := lec.db.Exec(fmt.Sprintf("INSERT INTO notifications (patron_id, message) SELECT patron_id, 'Event cancelled' FROM %s", tempTable))
	if err != nil {
		return err
	}

	return nil
}

func (lec *LibraryEventsController) notifyPatrons(tempTable string) error {
	// Notify affected patrons of schedule conflicts
	_, err := lec.db.Exec(fmt.Sprintf("INSERT INTO notifications (patron_id, message) SELECT patron_id, 'Event rescheduled' FROM %s", tempTable))
	if err != nil {
		return err
	}

	return nil
}

func (lec *LibraryEventsController) updateAttendanceStatus(tempTable string, status string) error {
	// Update the attendance status of affected registrants
	_, err := lec.db.Exec(fmt.Sprintf("UPDATE registrations SET attendance_status = '%s' WHERE event_id IN (SELECT event_id FROM %s)", status, tempTable))
	if err != nil {
		return err
	}

	return nil
}