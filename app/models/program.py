

from datetime import date
from typing import Optional

class Program:
    def __init__(self, program_id: int, program_name: str, program_status: str, program_start_date: date, program_end_date: date, capacity: int):
        if not isinstance(program_start_date, date) or not isinstance(program_end_date, date):
            raise ValueError("program_start_date and program_end_date must be date objects")
        if program_start_date > program_end_date:
            raise ValueError("program_start_date cannot be after program_end_date")
        if capacity < 0:
            raise ValueError("capacity cannot be negative")
        self.program_id = program_id
        self.program_name = program_name
        self.program_status = program_status
        self.program_start_date = program_start_date
        self.program_end_date = program_end_date
        self.capacity = capacity

    def is_active(self) -> bool:
        return self.program_status == "active"

    def is_full(self) -> bool:
        return self.capacity == 0

    def update_status(self, new_status: str) -> None:
        self.program_status = new_status

    def update_capacity(self, new_capacity: int) -> None:
        if new_capacity < 0:
            raise ValueError("capacity cannot be negative")
        self.capacity = new_capacity