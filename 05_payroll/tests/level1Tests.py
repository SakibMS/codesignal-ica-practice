import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from payroll import Payroll


class PayrollLevel1Test(unittest.TestCase):
    """
    Graded tests for level 1. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.payroll = Payroll()

    """
    Can't clock in twice, or clock out without clocking in.
    Unknown employees fail.
    """
    @timeout(0.1)
    def test_01_clockInAndOut(self):
        pr = self.payroll
        self.assertEqual(pr.add_employee(1, "e1", "eng", 10), True)
        self.assertEqual(pr.add_employee(2, "e1", "ops", 20), False)
        self.assertEqual(pr.clock_in(3, "e1"), True)
        self.assertEqual(pr.clock_in(4, "e1"), False)
        self.assertEqual(pr.clock_out(10, "e1"), 7)
        self.assertEqual(pr.clock_out(11, "e1"), None)
        self.assertEqual(pr.clock_in(12, "e2"), False)
        self.assertEqual(pr.clock_out(13, "e2"), None)

    """
    Sessions [3, 10) and [20, 25) -> 12. The ongoing session isn't counted.
    """
    @timeout(0.1)
    def test_02_workedTime(self):
        pr = self.payroll
        self.assertEqual(pr.add_employee(1, "a", "t", 5), True)
        self.assertEqual(pr.get_worked_time(2, "a"), 0)
        self.assertEqual(pr.clock_in(3, "a"), True)
        self.assertEqual(pr.get_worked_time(8, "a"), 0)
        self.assertEqual(pr.clock_out(10, "a"), 7)
        self.assertEqual(pr.clock_in(20, "a"), True)
        self.assertEqual(pr.clock_out(25, "a"), 5)
        self.assertEqual(pr.get_worked_time(30, "a"), 12)
        self.assertEqual(pr.get_worked_time(31, "b"), None)

    """
    Two employees with overlapping sessions are tracked separately.
    """
    @timeout(0.1)
    def test_03_multipleEmployees(self):
        pr = self.payroll
        self.assertEqual(pr.add_employee(1, "x", "t", 1), True)
        self.assertEqual(pr.add_employee(2, "y", "t", 1), True)
        self.assertEqual(pr.clock_in(3, "x"), True)
        self.assertEqual(pr.clock_in(4, "y"), True)
        self.assertEqual(pr.clock_out(9, "x"), 6)
        self.assertEqual(pr.clock_in(10, "x"), True)
        self.assertEqual(pr.clock_out(14, "y"), 10)
        self.assertEqual(pr.clock_out(15, "x"), 5)
        self.assertEqual(pr.get_worked_time(16, "x"), 11)
        self.assertEqual(pr.get_worked_time(17, "y"), 10)
