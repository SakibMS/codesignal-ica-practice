import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from payroll import Payroll


class PayrollLevel2Test(unittest.TestCase):
    """
    Graded tests for level 2. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.payroll = Payroll()

    """
    eng: ann 10, bob 20, cat 10. ops: dan 100.
    """
    @timeout(0.1)
    def test_01_topWorkers(self):
        pr = self.payroll
        pr.add_employee(1, "ann", "eng", 1)
        pr.add_employee(2, "bob", "eng", 1)
        pr.add_employee(3, "cat", "eng", 1)
        pr.add_employee(4, "dan", "ops", 1)
        pr.clock_in(5, "ann")
        self.assertEqual(pr.clock_out(15, "ann"), 10)
        pr.clock_in(16, "bob")
        self.assertEqual(pr.clock_out(36, "bob"), 20)
        pr.clock_in(37, "cat")
        self.assertEqual(pr.clock_out(47, "cat"), 10)
        pr.clock_in(48, "dan")
        self.assertEqual(pr.clock_out(148, "dan"), 100)
        self.assertEqual(pr.top_workers(150, "eng", 2), ["bob(20)", "ann(10)"])
        self.assertEqual(pr.top_workers(151, "eng", 5), ["bob(20)", "ann(10)", "cat(10)"])
        self.assertEqual(pr.top_workers(152, "ops", 1), ["dan(100)"])
        self.assertEqual(pr.top_workers(153, "hr", 3), [])

    """
    q's session only counts once it is completed.
    """
    @timeout(0.1)
    def test_02_ongoingSessionNotCounted(self):
        pr = self.payroll
        pr.add_employee(1, "p", "a", 1)
        pr.add_employee(2, "q", "a", 1)
        pr.clock_in(3, "p")
        self.assertEqual(pr.clock_out(5, "p"), 2)
        self.assertEqual(pr.clock_in(6, "q"), True)
        self.assertEqual(pr.top_workers(100, "a", 2), ["p(2)", "q(0)"])
        self.assertEqual(pr.clock_out(101, "q"), 95)
        self.assertEqual(pr.top_workers(102, "a", 2), ["q(95)", "p(2)"])

    """
    Team totals, sorted by total then team name.
    """
    @timeout(0.1)
    def test_03_teamTotals(self):
        pr = self.payroll
        pr.add_employee(1, "a1", "alpha", 1)
        pr.add_employee(2, "a2", "alpha", 1)
        pr.add_employee(3, "b1", "beta", 1)
        pr.add_employee(4, "c1", "gamma", 1)
        self.assertEqual(pr.team_totals(5), ["alpha(0)", "beta(0)", "gamma(0)"])
        pr.clock_in(6, "a1")
        self.assertEqual(pr.clock_out(16, "a1"), 10)
        pr.clock_in(17, "b1")
        self.assertEqual(pr.clock_out(32, "b1"), 15)
        pr.clock_in(33, "a2")
        self.assertEqual(pr.clock_out(38, "a2"), 5)
        self.assertEqual(pr.team_totals(40), ["alpha(15)", "beta(15)", "gamma(0)"])
        pr.clock_in(41, "c1")
        self.assertEqual(pr.clock_out(61, "c1"), 20)
        self.assertEqual(pr.team_totals(62), ["gamma(20)", "alpha(15)", "beta(15)"])
