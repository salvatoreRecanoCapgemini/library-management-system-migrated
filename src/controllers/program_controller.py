

from src.services.program_service import ProgramService
from src.repositories.program_repository import ProgramRepository
from src.db.session import db_session
import logging

class ProgramLifecycleController:
    def __init__(self):
        self.program_service = ProgramService(ProgramRepository(db_session))
        self.logger = logging.getLogger(__name__)

    def manage_program_lifecycle(self, program_id, action, params):
        """
        Handles HTTP requests for managing the program lifecycle.

        Args:
            program_id (int): The ID of the program.
            action (str): The action to perform on the program.
            params (dict): Additional parameters for the action.

        Returns:
            The result of the program lifecycle management.
        """
        if not isinstance(program_id, int) or program_id <= 0:
            self.logger.error("Invalid program ID")
            return {"error": "Invalid program ID"}
        if not isinstance(action, str) or not action:
            self.logger.error("Invalid action")
            return {"error": "Invalid action"}
        if not isinstance(params, dict):
            self.logger.error("Invalid parameters")
            return {"error": "Invalid parameters"}
        try:
            return self.program_service.manage_program_lifecycle(program_id, action, params)
        except Exception as e:
            self.logger.error(f"Error managing program lifecycle: {str(e)}")
            return {"error": "Error managing program lifecycle"}

    def start_program(self, program_id, action, params):
        """
        Handles HTTP requests for starting a program.

        Args:
            program_id (int): The ID of the program.
            action (str): The action to perform on the program.
            params (dict): Additional parameters for the action.

        Returns:
            The result of starting the program.
        """
        if not isinstance(program_id, int) or program_id <= 0:
            self.logger.error("Invalid program ID")
            return {"error": "Invalid program ID"}
        if not isinstance(action, str) or not action:
            self.logger.error("Invalid action")
            return {"error": "Invalid action"}
        if not isinstance(params, dict):
            self.logger.error("Invalid parameters")
            return {"error": "Invalid parameters"}
        try:
            return self.program_service.start_program(program_id, action, params)
        except Exception as e:
            self.logger.error(f"Error starting program: {str(e)}")
            return {"error": "Error starting program"}

    def record_attendance(self, program_id, action, params):
        """
        Handles HTTP requests for recording attendance for a program.

        Args:
            program_id (int): The ID of the program.
            action (str): The action to perform on the program.
            params (dict): Additional parameters for the action.

        Returns:
            The result of recording attendance for the program.
        """
        if not isinstance(program_id, int) or program_id <= 0:
            self.logger.error("Invalid program ID")
            return {"error": "Invalid program ID"}
        if not isinstance(action, str) or not action:
            self.logger.error("Invalid action")
            return {"error": "Invalid action"}
        if not isinstance(params, dict):
            self.logger.error("Invalid parameters")
            return {"error": "Invalid parameters"}
        try:
            return self.program_service.record_attendance(program_id, action, params)
        except Exception as e:
            self.logger.error(f"Error recording attendance: {str(e)}")
            return {"error": "Error recording attendance"}

    def complete_program(self, program_id, action, params):
        """
        Handles HTTP requests for completing a program.

        Args:
            program_id (int): The ID of the program.
            action (str): The action to perform on the program.
            params (dict): Additional parameters for the action.

        Returns:
            The result of completing the program.
        """
        if not isinstance(program_id, int) or program_id <= 0:
            self.logger.error("Invalid program ID")
            return {"error": "Invalid program ID"}
        if not isinstance(action, str) or not action:
            self.logger.error("Invalid action")
            return {"error": "Invalid action"}
        if not isinstance(params, dict):
            self.logger.error("Invalid parameters")
            return {"error": "Invalid parameters"}
        try:
            return self.program_service.complete_program(program_id, action, params)
        except Exception as e:
            self.logger.error(f"Error completing program: {str(e)}")
            return {"error": "Error completing program"}