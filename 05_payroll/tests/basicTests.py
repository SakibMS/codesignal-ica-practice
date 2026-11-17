import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from payroll import Payroll


class PayrollBasicTest(unittest.TestCase):
    """
    Playground: add your own tests here (e.g. the examples from each
    level's spec). These results are shown but don't count toward
    your score.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.payroll = Payroll()

    """
    Example from spec/level1.md
    """
    @timeout(0.1)
    def test_level1_example(self):
        pr = self.payroll
        self.assertEqual(pr.add_employee(1, "ann", "eng", 10), True)
        self.assertEqual(pr.clock_in(2, "ann"), True)
        self.assertEqual(pr.clock_in(3, "ann"), False)
        self.assertEqual(pr.clock_out(12, "ann"), 10)
        self.assertEqual(pr.get_worked_time(13, "ann"), 10)
        self.assertEqual(pr.clock_out(14, "ann"), None)
