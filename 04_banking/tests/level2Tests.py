import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from banking import Bank


class BankLevel2Test(unittest.TestCase):
    """
    Graded tests for level 2. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.bank = Bank()

    """
    Outgoing: a withdraws 300, b sends 500, c sends 200 (then withdraws 300).
    Incoming money doesn't count.
    """
    @timeout(0.1)
    def test_01_topSpenders(self):
        bank = self.bank
        for t, account in enumerate(["a", "b", "c"], start=1):
            bank.create_account(t, account)
        for t, account in enumerate(["a", "b", "c"], start=4):
            bank.deposit(t, account, 1000)
        self.assertEqual(bank.withdraw(7, "a", 300), 700)
        self.assertEqual(bank.transfer(8, "b", "c", 500), 500)
        self.assertEqual(bank.transfer(9, "c", "a", 200), 1300)
        self.assertEqual(bank.top_spenders(10, 3), ["b(500)", "a(300)", "c(200)"])
        self.assertEqual(bank.top_spenders(11, 1), ["b(500)"])
        self.assertEqual(bank.withdraw(12, "c", 300), 1000)
        self.assertEqual(bank.top_spenders(13, 2), ["b(500)", "c(500)"])

    """
    Accounts with nothing outgoing show 0.
    Failed withdrawals/transfers and deposits don't count.
    """
    @timeout(0.1)
    def test_02_failedOperationsDontCount(self):
        bank = self.bank
        bank.create_account(1, "x")
        bank.create_account(2, "y")
        bank.create_account(3, "z")
        self.assertEqual(bank.top_spenders(4, 5), ["x(0)", "y(0)", "z(0)"])
        self.assertEqual(bank.deposit(5, "y", 50), 50)
        self.assertEqual(bank.withdraw(6, "y", 60), None)
        self.assertEqual(bank.transfer(7, "y", "x", 70), None)
        self.assertEqual(bank.transfer(8, "y", "x", 50), 0)
        self.assertEqual(bank.top_spenders(9, 2), ["y(50)", "x(0)"])
        self.assertEqual(bank.deposit(10, "z", 999), 999)
        self.assertEqual(bank.top_spenders(11, 3), ["y(50)", "x(0)", "z(0)"])

    """
    acc1..acc12 each withdraw 10. Ties sort as strings:
    acc1 < acc10 < acc11 < acc12 < acc2 < ...
    """
    @timeout(0.1)
    def test_03_tiesSortAsStrings(self):
        bank = self.bank
        for i in range(1, 13):
            account = f"acc{i}"
            bank.create_account(3 * i, account)
            bank.deposit(3 * i + 1, account, 100)
            self.assertEqual(bank.withdraw(3 * i + 2, account, 10), 90)
        self.assertEqual(
            bank.top_spenders(100, 5),
            ["acc1(10)", "acc10(10)", "acc11(10)", "acc12(10)", "acc2(10)"]
        )
        self.assertEqual(bank.withdraw(101, "acc7", 5), 85)
        self.assertEqual(bank.top_spenders(102, 2), ["acc7(15)", "acc1(10)"])
