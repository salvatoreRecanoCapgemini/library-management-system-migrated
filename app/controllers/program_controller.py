

from flask import request, jsonify
from app.services.program_service import ProgramService, manage_program_lifecycle

class ProgramController:
    def __init__(self):
        self.program_service = ProgramService()

    def log_program_state_change(self, program_id, action, params):
        try:
            self.program_service.log_program_state_change(program_id, action, params)
            manage_program_lifecycle(program_id, action, params)
            return jsonify({'message': 'Program state change logged successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def start_program(self, program_id):
        try:
            self.program_service.start_program(program_id)
            self.log_program_state_change(program_id, 'START_PROGRAM', {})
            return jsonify({'message': 'Program started successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def record_attendance(self, program_id, params):
        try:
            self.program_service.record_attendance(program_id, params)
            self.log_program_state_change(program_id, 'RECORD_ATTENDANCE', params)
            return jsonify({'message': 'Attendance recorded successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def complete_program(self, program_id):
        try:
            self.program_service.complete_program(program_id)
            self.log_program_state_change(program_id, 'COMPLETE_PROGRAM', {})
            return jsonify({'message': 'Program completed successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/programs/<int:program_id>/start', methods=['POST'])
def start_program(program_id):
    controller = ProgramController()
    return controller.start_program(program_id)

@app.route('/programs/<int:program_id>/record_attendance', methods=['POST'])
def record_attendance(program_id):
    controller = ProgramController()
    params = request.get_json()
    return controller.record_attendance(program_id, params)

@app.route('/programs/<int:program_id>/complete', methods=['POST'])
def complete_program(program_id):
    controller = ProgramController()
    return controller.complete_program(program_id)