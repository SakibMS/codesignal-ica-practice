import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from payroll import Payroll


class PayrollLevel3Test(unittest.TestCase):
    """
    Graded tests for level 3. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.payroll = Payroll()

    """
    Rate 10. Sessions [10, 20) and [30, 35).
    [15, 32) overlaps 5 + 2 = 7 units -> 70.
    """
    @timeout(0.1)
    def test_01_payForRange(self):
        pr = self.payroll
        pr.add_employee(1, "e", "t", 10)
        pr.clock_in(10, "e")
        self.assertEqual(pr.clock_out(20, "e"), 10)
        pr.clock_in(30, "e")
        self.assertEqual(pr.clock_out(35, "e"), 5)
        self.assertEqual(pr.get_pay(40, "e", 0, 40), 150)
        self.assertEqual(pr.get_pay(41, "e", 15, 32), 70)
        self.assertEqual(pr.get_pay(42, "e", 20, 30), 0)
        self.assertEqual(pr.get_pay(43, "x", 0, 10), None)

    """
    [2, 12) at rate 10 = 100; rate -> 30 at 20; [22, 25) at 30 = 90.
    """
    @timeout(0.1)
    def test_02_rateChange(self):
        pr = self.payroll
        pr.add_employee(1, "e", "t", 10)
        pr.clock_in(2, "e")
        self.assertEqual(pr.clock_out(12, "e"), 10)
        self.assertEqual(pr.set_rate(20, "e", 30), True)
        self.assertEqual(pr.set_rate(21, "z", 30), False)
        pr.clock_in(22, "e")
        self.assertEqual(pr.clock_out(25, "e"), 3)
        self.assertEqual(pr.get_pay(30, "e", 0, 30), 190)
        self.assertEqual(pr.get_pay(31, "e", 10, 23), 50)

    """
    One session [10, 20) with rate 2, then 5 from 15, then 1 from 18:
    5 x 2 + 3 x 5 + 2 x 1 = 27.
    """
    @timeout(0.1)
    def test_03_rateChangeDuringSession(self):
        pr = self.payroll
        pr.add_employee(1, "e", "t", 2)
        pr.clock_in(10, "e")
        self.assertEqual(pr.set_rate(15, "e", 5), True)
        self.assertEqual(pr.set_rate(18, "e", 1), True)
        self.assertEqual(pr.clock_out(20, "e"), 10)
        self.assertEqual(pr.get_pay(21, "e", 0, 21), 27)
        self.assertEqual(pr.get_pay(22, "e", 12, 19), 22)
        self.assertEqual(pr.get_worked_time(23, "e"), 10)

    """
    An ongoing session isn't paid until it's completed.
    """
    @timeout(0.1)
    def test_04_ongoingSessionNotPaid(self):
        pr = self.payroll
        pr.add_employee(1, "e", "t", 3)
        pr.clock_in(5, "e")
        self.assertEqual(pr.get_pay(10, "e", 0, 10), 0)
        self.assertEqual(pr.clock_out(11, "e"), 6)
        self.assertEqual(pr.get_pay(12, "e", 0, 12), 18)
