

from flask import request, jsonify
from app.services import staff_service
import logging

def update_staff_status():
    try:
        staff_id = request.json['staff_id']
        new_status = request.json['new_status']
        if not staff_id or not new_status:
            return jsonify({'message': 'Staff ID and new status are required'}), 400
        if not isinstance(staff_id, int) or not isinstance(new_status, str):
            return jsonify({'message': 'Invalid input type'}), 400
        staff_service.update_staff_status(staff_id, new_status)
        logging.info(f'Staff status updated for staff ID {staff_id}')
        return jsonify({'message': 'Staff status updated successfully'})
    except KeyError as e:
        return jsonify({'message': 'Missing required field'}), 400
    except Exception as e:
        logging.error(f'Error updating staff status: {str(e)}')
        return jsonify({'message': 'Error updating staff status'}), 500