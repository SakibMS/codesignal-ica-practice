import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from payroll import Payroll


class PayrollLevel4Test(unittest.TestCase):
    """
    Graded tests for level 4. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.payroll = Payroll()

    """
    Rate 10, session [150, 250), bonus x2 on [100, 200):
    50 x 10 x 2 + 50 x 10 = 1500.
    Then a touching x3 bonus on [200, 220) is added retroactively:
    1000 + 20 x 30 + 30 x 10 = 1900.
    """
    @timeout(0.1)
    def test_01_bonusPeriod(self):
        pr = self.payroll
        pr.add_employee(1, "e", "t", 10)
        self.assertEqual(pr.add_bonus_period(2, 100, 200, 2), True)
        pr.clock_in(150, "e")
        self.assertEqual(pr.clock_out(250, "e"), 100)
        self.assertEqual(pr.get_pay(260, "e", 0, 300), 1500)
        self.assertEqual(pr.get_pay(261, "e", 190, 210), 300)
        self.assertEqual(pr.add_bonus_period(262, 150, 210, 3), False)
        self.assertEqual(pr.add_bonus_period(263, 200, 220, 3), True)
        self.assertEqual(pr.get_pay(264, "e", 0, 300), 1900)

    """
    Rate 1 -> 2 at 15, bonus x3 on [10, 20), session [5, 25):
    [5,10) 5 + [10,15) 15 + [15,20) 30 + [20,25) 10 = 60.
    """
    @timeout(0.1)
    def test_02_bonusAndRateChange(self):
        pr = self.payroll
        pr.add_employee(1, "e", "t", 1)
        self.assertEqual(pr.add_bonus_period(2, 10, 20, 3), True)
        pr.clock_in(5, "e")
        self.assertEqual(pr.set_rate(15, "e", 2), True)
        self.assertEqual(pr.clock_out(25, "e"), 20)
        self.assertEqual(pr.get_pay(30, "e", 0, 30), 60)
        self.assertEqual(pr.get_pay(31, "e", 12, 22), 43)

    """
    a: [4, 14) x 10 = 100. b: [15, 35) x 5 = 100. c: [36, 40) x 20 = 80.
    In [30, 50): c 80, b 25, a 0.
    A x4 bonus on [0, 10) lifts a to 6 x 40 + 4 x 10 = 280.
    """
    @timeout(0.1)
    def test_03_topEarners(self):
        pr = self.payroll
        pr.add_employee(1, "a", "x", 10)
        pr.add_employee(2, "b", "y", 5)
        pr.add_employee(3, "c", "x", 20)
        pr.clock_in(4, "a")
        self.assertEqual(pr.clock_out(14, "a"), 10)
        pr.clock_in(15, "b")
        self.assertEqual(pr.clock_out(35, "b"), 20)
        pr.clock_in(36, "c")
        self.assertEqual(pr.clock_out(40, "c"), 4)
        self.assertEqual(pr.top_earners(50, 3, 0, 50), ["a(100)", "b(100)", "c(80)"])
        self.assertEqual(pr.top_earners(51, 1, 30, 50), ["c(80)"])
        self.assertEqual(pr.top_earners(52, 2, 30, 50), ["c(80)", "b(25)"])
        self.assertEqual(pr.add_bonus_period(53, 0, 10, 4), True)
        self.assertEqual(pr.top_earners(54, 3, 0, 50), ["a(280)", "b(100)", "c(80)"])

    """
    Bonuses x2 on [10, 20) and x5 on [20, 30); overlapping ones are rejected.
    Rate 7, session [8, 32): 2x7 + 10x14 + 10x35 + 2x7 = 518.
    """
    @timeout(0.1)
    def test_04_adjacentBonuses(self):
        pr = self.payroll
        pr.add_employee(1, "e", "t", 7)
        pr.add_employee(2, "f", "t", 7)
        self.assertEqual(pr.add_bonus_period(3, 10, 20, 2), True)
        self.assertEqual(pr.add_bonus_period(4, 20, 30, 5), True)
        self.assertEqual(pr.add_bonus_period(5, 5, 11, 2), False)
        self.assertEqual(pr.add_bonus_period(6, 29, 40, 2), False)
        pr.clock_in(8, "e")
        self.assertEqual(pr.clock_out(32, "e"), 24)
        self.assertEqual(pr.get_pay(33, "e", 0, 40), 518)
        self.assertEqual(pr.top_earners(34, 2, 0, 40), ["e(518)", "f(0)"])
        self.assertEqual(pr.get_pay(35, "e", 20, 30), 350)
