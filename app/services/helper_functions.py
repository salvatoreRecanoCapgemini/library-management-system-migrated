

import logging
from typing import List, Dict
from app.models import Program, Registration, AttendanceRecord, CompletionStatistics
from app.repositories import ProgramRepository, AttendanceLogRepository, CompletionStatusRepository, StateChangeLogRepository
from app.notifications import AttendanceNotification

logger = logging.getLogger(__name__)

def create_waitlist_notification_batch(program: Program) -> None:
    try:
        # Create a waitlist notification batch
        # TO DO: implement the logic to create a waitlist notification batch
        pass
    except Exception as e:
        logger.error(f"Error creating waitlist notification batch: {str(e)}")

def update_program_status(program: Program, status: str) -> None:
    try:
        # Update the program status
        program_repository = ProgramRepository()
        program_repository.update_status(program, status)
    except Exception as e:
        logger.error(f"Error updating program status: {str(e)}")

def get_attendance_records(program: Program) -> List[AttendanceRecord]:
    try:
        # Retrieve attendance records for the program
        attendance_log_repository = AttendanceLogRepository()
        return attendance_log_repository.get_attendance_records(program)
    except Exception as e:
        logger.error(f"Error retrieving attendance records: {str(e)}")
        return []

def update_attendance_log(registration: Registration, params: Dict[str, object]) -> None:
    try:
        # Update the attendance log for the registration
        attendance_log_repository = AttendanceLogRepository()
        attendance_log_repository.update_log(registration, params)
    except Exception as e:
        logger.error(f"Error updating attendance log: {str(e)}")

def generate_attendance_notification(program: Program, params: Dict[str, object]) -> None:
    try:
        # Generate an attendance notification for the program
        attendance_notification = AttendanceNotification()
        attendance_notification.generate_notification(program, params)
    except Exception as e:
        logger.error(f"Error generating attendance notification: {str(e)}")

def calculate_completion_statistics(program: Program) -> CompletionStatistics:
    try:
        # Calculate completion statistics for the program
        # TO DO: implement the logic to calculate completion statistics
        return CompletionStatistics()
    except Exception as e:
        logger.error(f"Error calculating completion statistics: {str(e)}")
        return CompletionStatistics()

def update_completion_status(program: Program, completion_statistics: CompletionStatistics) -> None:
    try:
        # Update completion status for participants
        completion_status_repository = CompletionStatusRepository()
        completion_status_repository.update_status(program, completion_statistics)
    except Exception as e:
        logger.error(f"Error updating completion status: {str(e)}")

def log_state_change(program_id: int, action: str, params: Dict[str, object]) -> None:
    try:
        # Log the program state change
        state_change_log_repository = StateChangeLogRepository()
        state_change_log_repository.log_change(program_id, action, params)
    except Exception as e:
        logger.error(f"Error logging state change: {str(e)}")