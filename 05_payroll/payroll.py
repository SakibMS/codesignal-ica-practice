from typing import Optional


class Payroll:
    """
    Time tracking and payroll. The task is described in spec/level1.md.
    Add the methods for later levels as you unlock them.
    """

    def __init__(self):
        # TODO: set up your data structures
        pass

    def add_employee(self, timestamp: int, employee_id: str, team: str, rate: int) -> bool:
        """
        Adds an employee in `team` who earns `rate` per unit of time.

        :return: True if added, False if `employee_id` already exists.
        """
        # TODO: implement this method
        return False

    def clock_in(self, timestamp: int, employee_id: str) -> bool:
        """
        Starts a work session.

        :return: True on success, False if the employee doesn't exist
                 or is already clocked in.
        """
        # TODO: implement this method
        return False

    def clock_out(self, timestamp: int, employee_id: str) -> Optional[int]:
        """
        Ends the current work session.

        :return: the session's length, or None if the employee doesn't
                 exist or isn't clocked in.
        """
        # TODO: implement this method
        return None

    def get_worked_time(self, timestamp: int, employee_id: str) -> Optional[int]:
        """
        :return: the total length of completed sessions, or None if the
                 employee doesn't exist.
        """
        # TODO: implement this method
        return None
