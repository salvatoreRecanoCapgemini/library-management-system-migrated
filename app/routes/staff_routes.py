

from flask import request, jsonify
from app.services.staff_service import StaffService

staff_service = StaffService('postgresql://user:password@host:port/dbname')

@app.route('/update_staff_status', methods=['POST'])
def update_staff_status():
    if 'staff_id' not in request.json or 'new_status' not in request.json:
        return jsonify({'error': 'Missing required parameters'}), 400

    staff_id = request.json['staff_id']
    new_status = request.json['new_status']

    try:
        staff_service.update_status(staff_id, new_status)
        return jsonify({'message': 'Staff status updated successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating staff status'}), 500