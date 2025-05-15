

from flask import request, jsonify
from app.services.staff_service import update_staff_status

def update_staff_status_controller():
    staff_id = request.json.get('staff_id')
    new_status = request.json.get('new_status')

    if not staff_id or not new_status:
        return jsonify({'error': 'Invalid or empty staff_id or new_status'}), 400

    try:
        result = update_staff_status(staff_id, new_status)
        if result.get('success'):
            return jsonify({'message': 'Staff status updated successfully'}), 200
        elif result.get('error') == 'invalid_staff_id':
            return jsonify({'error': 'Staff ID does not exist'}), 404
        elif result.get('error') == 'invalid_status':
            return jsonify({'error': 'Invalid new status'}), 400
        else:
            return jsonify({'error': 'Failed to update staff status'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500