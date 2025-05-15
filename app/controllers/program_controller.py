

from flask import Blueprint, request, jsonify
from app.services.program_service import ProgramService
import logging

program_controller = Blueprint('program_controller', __name__)
program_service = ProgramService()
logger = logging.getLogger(__name__)

@program_controller.route('/programs/<int:program_id>/start', methods=['POST'])
def start_program(program_id):
    try:
        params = request.get_json()
        if not params:
            return jsonify({'message': 'Invalid request parameters'}), 400
        program_service.start_program(program_id, params)
        logger.info(f'Program {program_id} started successfully')
        return jsonify({'message': 'Program started successfully'}), 200
    except Exception as e:
        logger.error(f'Error starting program {program_id}: {str(e)}')
        return jsonify({'message': 'Error starting program'}), 500

@program_controller.route('/programs/<int:program_id>/attendance', methods=['POST'])
def record_attendance(program_id):
    try:
        params = request.get_json()
        if not params:
            return jsonify({'message': 'Invalid request parameters'}), 400
        program_service.record_attendance(program_id, params)
        logger.info(f'Attendance recorded for program {program_id}')
        return jsonify({'message': 'Attendance recorded successfully'}), 200
    except Exception as e:
        logger.error(f'Error recording attendance for program {program_id}: {str(e)}')
        return jsonify({'message': 'Error recording attendance'}), 500

@program_controller.route('/programs/<int:program_id>/complete', methods=['POST'])
def complete_program(program_id):
    try:
        program_service.complete_program(program_id)
        logger.info(f'Program {program_id} completed successfully')
        return jsonify({'message': 'Program completed successfully'}), 200
    except Exception as e:
        logger.error(f'Error completing program {program_id}: {str(e)}')
        return jsonify({'message': 'Error completing program'}), 500