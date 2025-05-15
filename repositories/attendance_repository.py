

package repositories

import (
	"errors"
	"fmt"
	"log"
)

const (
	PROGRAM_STATUS_IN_PROGRESS = "IN_PROGRESS"
	ATTENDANCE_STATUS_PRESENT   = "PRESENT"
)

type AttendanceRepository struct {
	programService        ProgramService
	notificationService   NotificationService
	attendanceLogService  AttendanceLogService
}

func NewAttendanceRepository(programService ProgramService, notificationService NotificationService, attendanceLogService AttendanceLogService) *AttendanceRepository {
	return &AttendanceRepository{
		programService:        programService,
		notificationService:   notificationService,
		attendanceLogService:  attendanceLogService,
	}
}

func (ar *AttendanceRepository) RecordAttendance(programID string, registrationID string) error {
	programData, err := ar.programService.GetProgramData(programID)
	if err != nil {
		return err
	}

	if programData.Status != PROGRAM_STATUS_IN_PROGRESS {
		return errors.New("invalid program status")
	}

	attendanceRecords, err := ar.programService.GetAttendanceRecords(programID)
	if err != nil {
		return err
	}

	for _, registration := range attendanceRecords {
		if registration.ID != registrationID {
			continue
		}

		err = ar.attendanceLogService.UpdateAttendanceLog(registrationID, ATTENDANCE_STATUS_PRESENT)
		if err != nil {
			return err
		}

		err = ar.notificationService.GenerateAttendanceNotification(registrationID, ATTENDANCE_STATUS_PRESENT)
		if err != nil {
			return err
		}
	}

	if len(attendanceRecords) == 0 {
		return errors.New("no attendance records found")
	}

	err = ar.attendanceLogService.LogAttendanceRecording(programID, registrationID, ATTENDANCE_STATUS_PRESENT)
	if err != nil {
		return err
	}

	return nil
}

type ProgramService interface {
	GetProgramData(programID string) (*ProgramData, error)
	GetAttendanceRecords(programID string) ([]Registration, error)
}

type ProgramData struct {
	Status string
}

type Registration struct {
	ID string
}

type NotificationService interface {
	GenerateAttendanceNotification(registrationID string, attendanceStatus string) error
}

type AttendanceLogService interface {
	UpdateAttendanceLog(registrationID string, attendanceStatus string) error
	LogAttendanceRecording(programID string, registrationID string, attendanceStatus string) error
}

type ProgramServiceMock struct{}

func (ps *ProgramServiceMock) GetProgramData(programID string) (*ProgramData, error) {
	return &ProgramData{Status: PROGRAM_STATUS_IN_PROGRESS}, nil
}

func (ps *ProgramServiceMock) GetAttendanceRecords(programID string) ([]Registration, error) {
	return []Registration{{ID: "registration-1"}}, nil
}

type NotificationServiceMock struct{}

func (ns *NotificationServiceMock) GenerateAttendanceNotification(registrationID string, attendanceStatus string) error {
	return nil
}

type AttendanceLogServiceMock struct{}

func (als *AttendanceLogServiceMock) UpdateAttendanceLog(registrationID string, attendanceStatus string) error {
	return nil
}

func (als *AttendanceLogServiceMock) LogAttendanceRecording(programID string, registrationID string, attendanceStatus string) error {
	return nil
}

func main() {
	programService := &ProgramServiceMock{}
	notificationService := &NotificationServiceMock{}
	attendanceLogService := &AttendanceLogServiceMock{}

	attendanceRepository := NewAttendanceRepository(programService, notificationService, attendanceLogService)

	err := attendanceRepository.RecordAttendance("program-1", "registration-1")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Attendance recorded successfully")
}