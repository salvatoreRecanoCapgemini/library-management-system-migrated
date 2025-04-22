

package src.models

class Program:
  def __init__(self, program_id, name, status, session_schedule, minimum_participants):
    if not isinstance(program_id, int) or program_id <= 0:
      raise ValueError("Program ID must be a positive integer")
    if not isinstance(name, str) or len(name) == 0:
      raise ValueError("Program name must be a non-empty string")
    if not isinstance(status, str) or len(status) == 0:
      raise ValueError("Program status must be a non-empty string")
    if not isinstance(session_schedule, str) or len(session_schedule) == 0:
      raise ValueError("Session schedule must be a non-empty string")
    if not isinstance(minimum_participants, int) or minimum_participants <= 0:
      raise ValueError("Minimum participants must be a positive integer")
    self.program_id = program_id
    self.name = name
    self.status = status
    self.session_schedule = session_schedule
    self.minimum_participants = minimum_participants