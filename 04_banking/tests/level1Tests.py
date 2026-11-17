import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from banking import Bank


class BankLevel1Test(unittest.TestCase):
    """
    Graded tests for level 1. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.bank = Bank()

    """
    Create accounts and deposit. Unknown accounts -> None.
    """
    @timeout(0.1)
    def test_01_createAndDeposit(self):
        bank = self.bank
        self.assertEqual(bank.create_account(1, "acc1"), True)
        self.assertEqual(bank.create_account(2, "acc1"), False)
        self.assertEqual(bank.create_account(3, "acc2"), True)
        self.assertEqual(bank.deposit(4, "acc1", 100), 100)
        self.assertEqual(bank.deposit(5, "acc1", 50), 150)
        self.assertEqual(bank.deposit(6, "acc3", 10), None)
        self.assertEqual(bank.get_balance(7, "acc1"), 150)
        self.assertEqual(bank.get_balance(8, "acc2"), 0)
        self.assertEqual(bank.get_balance(9, "acc3"), None)

    """
    Withdrawals can't exceed the balance; withdrawing everything leaves 0.
    """
    @timeout(0.1)
    def test_02_withdraw(self):
        bank = self.bank
        self.assertEqual(bank.create_account(1, "a"), True)
        self.assertEqual(bank.deposit(2, "a", 500), 500)
        self.assertEqual(bank.withdraw(3, "a", 200), 300)
        self.assertEqual(bank.withdraw(4, "a", 301), None)
        self.assertEqual(bank.withdraw(5, "a", 300), 0)
        self.assertEqual(bank.withdraw(6, "b", 1), None)
        self.assertEqual(bank.get_balance(7, "a"), 0)

    """
    Transfers return the source balance. Invalid transfers change nothing.
    """
    @timeout(0.1)
    def test_03_transfer(self):
        bank = self.bank
        self.assertEqual(bank.create_account(1, "alice"), True)
        self.assertEqual(bank.create_account(2, "bob"), True)
        self.assertEqual(bank.deposit(3, "alice", 1000), 1000)
        self.assertEqual(bank.transfer(4, "alice", "bob", 400), 600)
        self.assertEqual(bank.get_balance(5, "bob"), 400)
        self.assertEqual(bank.transfer(6, "bob", "alice", 500), None)
        self.assertEqual(bank.transfer(7, "alice", "alice", 10), None)
        self.assertEqual(bank.transfer(8, "alice", "carol", 10), None)
        self.assertEqual(bank.transfer(9, "carol", "alice", 10), None)
        self.assertEqual(bank.transfer(10, "bob", "alice", 400), 0)
        self.assertEqual(bank.get_balance(11, "alice"), 1000)
