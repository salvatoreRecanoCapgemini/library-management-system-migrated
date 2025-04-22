

package models

class Staff:
    def __init__(self, staff_id: int, status: str):
        if not isinstance(staff_id, int):
            raise TypeError("staff_id must be an integer")
        if not isinstance(status, str):
            raise TypeError("status must be a string")
        self.staff_id = staff_id
        self.status = status