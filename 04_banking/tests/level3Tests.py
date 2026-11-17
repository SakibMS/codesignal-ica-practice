import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from banking import Bank


class BankLevel3Test(unittest.TestCase):
    """
    Graded tests for level 3. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.bank = Bank()

    """
    payment1 (40) runs at 13 and counts as outgoing.
    """
    @timeout(0.1)
    def test_01_paymentRuns(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.deposit(2, "a", 100)
        self.assertEqual(bank.schedule_payment(3, "a", 40, 10), "payment1")
        self.assertEqual(bank.schedule_payment(4, "b", 40, 10), None)
        self.assertEqual(bank.get_payment_status(5, "a", "payment1"), "PENDING")
        self.assertEqual(bank.get_balance(12, "a"), 100)
        self.assertEqual(bank.get_balance(13, "a"), 60)
        self.assertEqual(bank.get_payment_status(14, "a", "payment1"), "COMPLETED")
        self.assertEqual(bank.top_spenders(15, 1), ["a(40)"])

    """
    payment1 (70) and payment2 (50) are both due at 23: payment1 runs first,
    so payment2 fails. Later, payment4 (due 39) runs before payment3 (due 43).
    """
    @timeout(0.1)
    def test_02_orderAndFailures(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.deposit(2, "a", 100)
        self.assertEqual(bank.schedule_payment(3, "a", 70, 20), "payment1")
        self.assertEqual(bank.schedule_payment(4, "a", 50, 19), "payment2")
        self.assertEqual(bank.get_balance(30, "a"), 30)
        self.assertEqual(bank.get_payment_status(31, "a", "payment1"), "COMPLETED")
        self.assertEqual(bank.get_payment_status(32, "a", "payment2"), "FAILED")
        self.assertEqual(bank.schedule_payment(33, "a", 30, 10), "payment3")
        self.assertEqual(bank.schedule_payment(34, "a", 20, 5), "payment4")
        self.assertEqual(bank.get_balance(50, "a"), 10)
        self.assertEqual(bank.get_payment_status(51, "a", "payment3"), "FAILED")
        self.assertEqual(bank.get_payment_status(52, "a", "payment4"), "COMPLETED")

    """
    Only the owner can cancel, and only while pending.
    payment2 is due at 28, so it has already run when cancel is called at 28.
    """
    @timeout(0.1)
    def test_03_cancel(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.create_account(2, "b")
        bank.deposit(3, "a", 100)
        self.assertEqual(bank.schedule_payment(4, "a", 30, 10), "payment1")
        self.assertEqual(bank.cancel_payment(5, "b", "payment1"), False)
        self.assertEqual(bank.cancel_payment(6, "a", "payment9"), False)
        self.assertEqual(bank.cancel_payment(7, "a", "payment1"), True)
        self.assertEqual(bank.cancel_payment(8, "a", "payment1"), False)
        self.assertEqual(bank.get_balance(20, "a"), 100)
        self.assertEqual(bank.get_payment_status(21, "a", "payment1"), "CANCELED")
        self.assertEqual(bank.get_payment_status(22, "b", "payment1"), None)
        self.assertEqual(bank.schedule_payment(23, "a", 10, 5), "payment2")
        self.assertEqual(bank.cancel_payment(28, "a", "payment2"), False)
        self.assertEqual(bank.get_balance(29, "a"), 90)

    """
    Payments run before other operations at the same timestamp:
    at 10, payment1 (80) fails before the deposit lands;
    at 20, payment2 (100) runs before the transfer, which then fails.
    """
    @timeout(0.1)
    def test_04_paymentsRunFirst(self):
        bank = self.bank
        bank.create_account(1, "a")
        bank.create_account(2, "b")
        bank.deposit(3, "a", 50)
        self.assertEqual(bank.schedule_payment(4, "a", 80, 6), "payment1")
        self.assertEqual(bank.deposit(10, "a", 100), 150)
        self.assertEqual(bank.get_payment_status(11, "a", "payment1"), "FAILED")
        self.assertEqual(bank.schedule_payment(12, "a", 100, 8), "payment2")
        self.assertEqual(bank.transfer(20, "a", "b", 100), None)
        self.assertEqual(bank.get_balance(21, "a"), 50)
        self.assertEqual(bank.top_spenders(22, 2), ["a(100)", "b(0)"])
