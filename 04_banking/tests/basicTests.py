import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from banking import Bank


class BankBasicTest(unittest.TestCase):
    """
    Playground: add your own tests here (e.g. the examples from each
    level's spec). These results are shown but don't count toward
    your score.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.bank = Bank()

    """
    Example from spec/level1.md
    """
    @timeout(0.1)
    def test_level1_example(self):
        bank = self.bank
        self.assertEqual(bank.create_account(1, "alice"), True)
        self.assertEqual(bank.create_account(2, "alice"), False)
        self.assertEqual(bank.create_account(3, "bob"), True)
        self.assertEqual(bank.deposit(4, "alice", 500), 500)
        self.assertEqual(bank.withdraw(5, "alice", 600), None)
        self.assertEqual(bank.transfer(6, "alice", "bob", 200), 300)
        self.assertEqual(bank.get_balance(7, "bob"), 200)
