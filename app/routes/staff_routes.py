

from flask import request, jsonify
from app.services import StaffService

@app.route('/staff/<int:staff_id>/status', methods=['PUT'])
def update_staff_status(staff_id):
    try:
        new_status = request.json['new_status']
        if new_status not in ['active', 'inactive']:
            return jsonify({'error': 'Invalid status'}), 400
        staff_service = StaffService()
        staff = staff_service.get_staff(staff_id)
        if staff is None:
            return jsonify({'error': 'Staff member not found'}), 404
        staff_service.update_staff_status(staff_id, new_status)
        return jsonify({'message': f'Staff {staff_id} status updated to {new_status}'}), 200
    except KeyError:
        return jsonify({'error': 'Missing new_status in request body'}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update staff status'}), 500