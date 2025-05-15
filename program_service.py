

package program_service

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log"
	"sync"

	"github.com/lib/pq"
)

type ProgramService struct {
	db *sql.DB
}

func NewProgramService(db *sql.DB) *ProgramService {
	return &ProgramService{db: db}
}

func (s *ProgramService) manageProgramLifecycle(ctx context.Context, programID int, action string, params map[string]interface{}) error {
	// Retrieve program status tracking data
	program, err := s.getProgram(ctx, programID)
	if err != nil {
		return err
	}

	// Perform the specified action on the program
	switch action {
	case "start":
		err = s.startProgram(ctx, program)
	case "record_attendance":
		err = s.recordAttendance(ctx, program, params)
	case "complete":
		err = s.completeProgram(ctx, program)
	default:
		return errors.New("invalid action")
	}

	if err != nil {
		return err
	}

	// Log the program state change
	err = s.logProgramStateChange(ctx, programID, action)
	if err != nil {
		return err
	}

	return nil
}

func (s *ProgramService) startProgram(ctx context.Context, program *Program) error {
	// Check if the program is in the 'PUBLISHED' status
	if program.Status != "PUBLISHED" {
		return errors.New("program is not in published status")
	}

	// Check if the program has sufficient registrations
	if program.Registrations < program.Capacity {
		return errors.New("program does not have sufficient registrations")
	}

	// Initialize the session schedule
	err := s.initSessionSchedule(ctx, program)
	if err != nil {
		return err
	}

	// Update the program status to 'IN_PROGRESS'
	_, err = s.db.ExecContext(ctx, "UPDATE programs SET status = 'IN_PROGRESS' WHERE id = $1", program.ID)
	if err != nil {
		return err
	}

	return nil
}

func (s *ProgramService) recordAttendance(ctx context.Context, program *Program, params map[string]interface{}) error {
	// Check if the program is in the 'IN_PROGRESS' status
	if program.Status != "IN_PROGRESS" {
		return errors.New("program is not in progress status")
	}

	// Retrieve attendance records for the program
	attendanceRecords, err := s.getAttendanceRecords(ctx, program.ID)
	if err != nil {
		return err
	}

	// Update attendance logs for each registration
	for _, attendanceRecord := range attendanceRecords {
		err = s.updateAttendanceLog(ctx, attendanceRecord, params)
		if err != nil {
			return err
		}
	}

	// Generate an attendance notification for each registration
	for _, attendanceRecord := range attendanceRecords {
		err = s.generateAttendanceNotification(ctx, attendanceRecord)
		if err != nil {
			return err
		}
	}

	return nil
}

func (s *ProgramService) completeProgram(ctx context.Context, program *Program) error {
	// Check if the program is in the 'IN_PROGRESS' status
	if program.Status != "IN_PROGRESS" {
		return errors.New("program is not in progress status")
	}

	// Calculate completion statistics
	completionStats, err := s.calculateCompletionStats(ctx, program)
	if err != nil {
		return err
	}

	// Update completion status for participants
	err = s.updateCompletionStatus(ctx, program, completionStats)
	if err != nil {
		return err
	}

	// Update the program status to 'COMPLETED'
	_, err = s.db.ExecContext(ctx, "UPDATE programs SET status = 'COMPLETED' WHERE id = $1", program.ID)
	if err != nil {
		return err
	}

	return nil
}

func (s *ProgramService) getProgram(ctx context.Context, programID int) (*Program, error) {
	var program Program
	err := s.db.QueryRowContext(ctx, "SELECT * FROM programs WHERE id = $1", programID).Scan(&program.ID, &program.Name, &program.Status, &program.Registrations, &program.Capacity)
	if err != nil {
		return nil, err
	}
	return &program, nil
}

func (s *ProgramService) initSessionSchedule(ctx context.Context, program *Program) error {
	// Initialize session schedule logic
	// Create a new transaction
	tx, err := s.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return err
	}

	// Initialize session schedule
	_, err = tx.ExecContext(ctx, "INSERT INTO session_schedules (program_id, start_date, end_date) VALUES ($1, $2, $3)", program.ID, program.StartDate, program.EndDate)
	if err != nil {
		tx.Rollback()
		return err
	}

	// Commit the transaction
	err = tx.Commit()
	if err != nil {
		return err
	}

	return nil
}

func (s *ProgramService) getAttendanceRecords(ctx context.Context, programID int) ([]AttendanceRecord, error) {
	var attendanceRecords []AttendanceRecord
	rows, err := s.db.QueryContext(ctx, "SELECT * FROM attendance_records WHERE program_id = $1", programID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var attendanceRecord AttendanceRecord
		err = rows.Scan(&attendanceRecord.ID, &attendanceRecord.ProgramID, &attendanceRecord.RegistrationID, &attendanceRecord.Attendance)
		if err != nil {
			return nil, err
		}
		attendanceRecords = append(attendanceRecords, attendanceRecord)
	}

	return attendanceRecords, nil
}

func (s *ProgramService) updateAttendanceLog(ctx context.Context, attendanceRecord AttendanceRecord, params map[string]interface{}) error {
	// Update attendance log logic
	// Create a new transaction
	tx, err := s.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return err
	}

	// Update attendance log
	_, err = tx.ExecContext(ctx, "UPDATE attendance_records SET attendance = $1 WHERE id = $2", attendanceRecord.Attendance, attendanceRecord.ID)
	if err != nil {
		tx.Rollback()
		return err
	}

	// Commit the transaction
	err = tx.Commit()
	if err != nil {
		return err
	}

	return nil
}

func (s *ProgramService) generateAttendanceNotification(ctx context.Context, attendanceRecord AttendanceRecord) error {
	// Generate attendance notification logic
	// Create a new transaction
	tx, err := s.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return err
	}

	// Generate attendance notification
	_, err = tx.ExecContext(ctx, "INSERT INTO attendance_notifications (attendance_record_id, notification_date) VALUES ($1, $2)", attendanceRecord.ID, attendanceRecord.NotificationDate)
	if err != nil {
		tx.Rollback()
		return err
	}

	// Commit the transaction
	err = tx.Commit()
	if err != nil {
		return err
	}

	return nil
}

func (s *ProgramService) calculateCompletionStats(ctx context.Context, program *Program) (*CompletionStats, error) {
	// Calculate completion statistics logic
	// Create a new transaction
	tx, err := s.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return nil, err
	}

	// Calculate completion statistics
	var completionStats CompletionStats
	err = tx.QueryRowContext(ctx, "SELECT COUNT(*) FROM attendance_records WHERE program_id = $1 AND attendance = TRUE", program.ID).Scan(&completionStats.CompletedRegistrations)
	if err != nil {
		tx.Rollback()
		return nil, err
	}

	// Commit the transaction
	err = tx.Commit()
	if err != nil {
		return nil, err
	}

	return &completionStats, nil
}

func (s *ProgramService) updateCompletionStatus(ctx context.Context, program *Program, completionStats *CompletionStats) error {
	// Update completion status logic
	// Create a new transaction
	tx, err := s.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return err
	}

	// Update completion status
	_, err = tx.ExecContext(ctx, "UPDATE programs SET completion_status = $1 WHERE id = $2", completionStats.CompletedRegistrations, program.ID)
	if err != nil {
		tx.Rollback()
		return err
	}

	// Commit the transaction
	err = tx.Commit()
	if err != nil {
		return err
	}

	return nil
}

func (s *ProgramService) logProgramStateChange(ctx context.Context, programID int, action string) error {
	// Log program state change logic
	// Create a new transaction
	tx, err := s.db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return err
	}

	// Log program state change
	_, err = tx.ExecContext(ctx, "INSERT INTO program_state_changes (program_id, action, timestamp) VALUES ($1, $2, $3)", programID, action, time.Now())
	if err != nil {
		tx.Rollback()
		return err
	}

	// Commit the transaction
	err = tx.Commit()
	if err != nil {
		return err
	}

	return nil
}

type Program struct {
	ID          int
	Name        string
	Status      string
	Registrations int
	Capacity    int
	StartDate   time.Time
	EndDate     time.Time
}

type AttendanceRecord struct {
	ID          int
	ProgramID   int
	RegistrationID int
	Attendance  bool
	NotificationDate time.Time
}

type CompletionStats struct {
	CompletedRegistrations int
}