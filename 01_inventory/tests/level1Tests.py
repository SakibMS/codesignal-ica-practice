import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from inventory import Inventory


class InventoryLevel1Test(unittest.TestCase):
    """
    Graded tests for level 1. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.inventory = Inventory()

    """
    Add apple and pear; adding apple again fails.
    Restock apple to 10, then 15. Restocking an unknown product -> None.
    """
    @timeout(0.1)
    def test_01_addAndRestock(self):
        inv = self.inventory
        self.assertEqual(inv.add_product(1, "apple", 50), True)
        self.assertEqual(inv.add_product(2, "apple", 60), False)
        self.assertEqual(inv.add_product(3, "pear", 70), True)
        self.assertEqual(inv.get_stock(4, "apple"), 0)
        self.assertEqual(inv.restock(5, "apple", 10), 10)
        self.assertEqual(inv.restock(6, "apple", 5), 15)
        self.assertEqual(inv.restock(7, "kiwi", 5), None)
        self.assertEqual(inv.get_stock(8, "apple"), 15)
        self.assertEqual(inv.get_stock(9, "pear"), 0)
        self.assertEqual(inv.get_stock(10, "kiwi"), None)

    """
    Restock pen to 10, sell 4 -> 6.
    Selling more than the stock fails and changes nothing.
    Selling the exact stock leaves 0.
    """
    @timeout(0.1)
    def test_02_sell(self):
        inv = self.inventory
        self.assertEqual(inv.add_product(1, "pen", 120), True)
        self.assertEqual(inv.restock(2, "pen", 10), 10)
        self.assertEqual(inv.sell(3, "pen", 4), 6)
        self.assertEqual(inv.sell(4, "pen", 7), None)
        self.assertEqual(inv.get_stock(5, "pen"), 6)
        self.assertEqual(inv.sell(6, "pen", 6), 0)
        self.assertEqual(inv.sell(7, "pen", 1), None)
        self.assertEqual(inv.sell(8, "pencil", 1), None)
        self.assertEqual(inv.get_stock(9, "pen"), 0)

    """
    Two products with interleaved operations.
    A sold-out product still exists.
    """
    @timeout(0.1)
    def test_03_mixedOperations(self):
        inv = self.inventory
        self.assertEqual(inv.add_product(1, "a", 10), True)
        self.assertEqual(inv.add_product(2, "b", 20), True)
        self.assertEqual(inv.restock(3, "a", 3), 3)
        self.assertEqual(inv.restock(4, "b", 8), 8)
        self.assertEqual(inv.sell(5, "b", 8), 0)
        self.assertEqual(inv.add_product(6, "b", 30), False)
        self.assertEqual(inv.restock(7, "b", 2), 2)
        self.assertEqual(inv.sell(8, "a", 1), 2)
        self.assertEqual(inv.sell(9, "a", 3), None)
        self.assertEqual(inv.get_stock(10, "a"), 2)
        self.assertEqual(inv.get_stock(11, "b"), 2)
