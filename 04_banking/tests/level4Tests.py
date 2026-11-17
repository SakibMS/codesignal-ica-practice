import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from banking import Bank


class BankLevel4Test(unittest.TestCase):
    """
    Graded tests for level 4. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.bank = Bank()

    """
    a (100) absorbs b (30, with 20 outgoing). b's id can be reused.
    """
    @timeout(0.1)
    def test_01_merge(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.create_account(2, "b")
        bank.deposit(3, "a", 100)
        bank.deposit(4, "b", 50)
        self.assertEqual(bank.withdraw(5, "b", 20), 30)
        self.assertEqual(bank.merge_accounts(6, "a", "b"), True)
        self.assertEqual(bank.get_balance(7, "a"), 130)
        self.assertEqual(bank.get_balance(8, "b"), None)
        self.assertEqual(bank.top_spenders(9, 5), ["a(20)"])
        self.assertEqual(bank.merge_accounts(10, "a", "a"), False)
        self.assertEqual(bank.merge_accounts(11, "a", "b"), False)
        self.assertEqual(bank.merge_accounts(12, "c", "a"), False)
        self.assertEqual(bank.create_account(13, "b"), True)
        self.assertEqual(bank.get_balance(14, "b"), 0)

    """
    b's pending payments move to a and are paid from a's balance.
    """
    @timeout(0.1)
    def test_02_mergeMovesPayments(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.create_account(2, "b")
        bank.deposit(3, "a", 10)
        bank.deposit(4, "b", 100)
        self.assertEqual(bank.schedule_payment(5, "b", 60, 10), "payment1")
        self.assertEqual(bank.schedule_payment(6, "b", 30, 20), "payment2")
        self.assertEqual(bank.merge_accounts(7, "a", "b"), True)
        self.assertEqual(bank.get_payment_status(8, "a", "payment1"), "PENDING")
        self.assertEqual(bank.get_payment_status(9, "b", "payment1"), None)
        self.assertEqual(bank.cancel_payment(10, "a", "payment2"), True)
        self.assertEqual(bank.get_balance(15, "a"), 50)
        self.assertEqual(bank.get_payment_status(16, "a", "payment1"), "COMPLETED")
        self.assertEqual(bank.top_spenders(17, 1), ["a(60)"])
        self.assertEqual(bank.get_balance(30, "a"), 50)

    """
    Balance history: 0 at 1, 100 at 2, 70 at 5, 80 at 9.
    """
    @timeout(0.1)
    def test_03_balanceAt(self):
        bank = self.bank
        bank.create_account(1, "a")
        self.assertEqual(bank.deposit(2, "a", 100), 100)
        self.assertEqual(bank.withdraw(5, "a", 30), 70)
        self.assertEqual(bank.deposit(9, "a", 10), 80)
        self.assertEqual(bank.get_balance_at(10, "a", 1), 0)
        self.assertEqual(bank.get_balance_at(11, "a", 2), 100)
        self.assertEqual(bank.get_balance_at(12, "a", 4), 100)
        self.assertEqual(bank.get_balance_at(13, "a", 5), 70)
        self.assertEqual(bank.get_balance_at(14, "a", 9), 80)
        self.assertEqual(bank.get_balance_at(15, "a", 0), None)
        self.assertEqual(bank.get_balance_at(16, "z", 5), None)
        self.assertEqual(bank.get_balance_at(17, "a", 17), 80)

    """
    The payment is due at 10 but first noticed at 20.
    History must still show the change at 10.
    """
    @timeout(0.1)
    def test_04_balanceAtWithPayments(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.deposit(2, "a", 100)
        self.assertEqual(bank.schedule_payment(3, "a", 40, 7), "payment1")
        self.assertEqual(bank.get_balance(20, "a"), 60)
        self.assertEqual(bank.get_balance_at(21, "a", 9), 100)
        self.assertEqual(bank.get_balance_at(22, "a", 10), 60)
        self.assertEqual(bank.get_balance_at(23, "a", 15), 60)

    """
    b is merged into a at 10, then re-created at 20.
    b's history: 200 before 10, None from 10 to 19, a new account from 20.
    """
    @timeout(0.1)
    def test_05_balanceAtAfterMerge(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.create_account(2, "b")
        bank.deposit(3, "a", 100)
        bank.deposit(4, "b", 200)
        self.assertEqual(bank.merge_accounts(10, "a", "b"), True)
        self.assertEqual(bank.get_balance_at(11, "a", 9), 100)
        self.assertEqual(bank.get_balance_at(12, "a", 10), 300)
        self.assertEqual(bank.get_balance_at(13, "b", 9), 200)
        self.assertEqual(bank.get_balance_at(14, "b", 10), None)
        self.assertEqual(bank.get_balance_at(15, "b", 15), None)
        self.assertEqual(bank.create_account(20, "b"), True)
        self.assertEqual(bank.deposit(21, "b", 5), 5)
        self.assertEqual(bank.get_balance_at(22, "b", 4), 200)
        self.assertEqual(bank.get_balance_at(23, "b", 15), None)
        self.assertEqual(bank.get_balance_at(24, "b", 21), 5)
