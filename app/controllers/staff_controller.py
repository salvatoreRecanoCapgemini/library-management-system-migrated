

from flask import request, jsonify
from app.services.staff_service import update_staff_status
from app import db

@app.route('/update_staff_status', methods=['POST'])
def update_staff_status():
    staff_id = request.json['staff_id']
    new_status = request.json['new_status']
    try:
        with db.session.begin():
            update_staff_status(staff_id, new_status)
        return jsonify({'message': 'Staff status updated successfully'})
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)})