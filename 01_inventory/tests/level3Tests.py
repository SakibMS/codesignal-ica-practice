import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from inventory import Inventory


class InventoryLevel3Test(unittest.TestCase):
    """
    Graded tests for level 3. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.inventory = Inventory()

    """
    Reserved units leave the stock right away.
    Ids count successful reservations only: res1, res2.
    """
    @timeout(0.1)
    def test_01_reserveHoldsStock(self):
        inv = self.inventory
        inv.add_product(1, "tv", 1000)
        inv.restock(2, "tv", 5)
        self.assertEqual(inv.reserve(3, "tv", 2, 100), "res1")
        self.assertEqual(inv.get_stock(4, "tv"), 3)
        self.assertEqual(inv.sell(5, "tv", 4), None)
        self.assertEqual(inv.reserve(6, "tv", 4, 100), None)
        self.assertEqual(inv.reserve(7, "radio", 1, 100), None)
        self.assertEqual(inv.reserve(8, "tv", 3, 50), "res2")
        self.assertEqual(inv.get_stock(9, "tv"), 0)

    """
    res1 (made at 3, duration 10) expires at 13: its units come back at 13
    and it can't be confirmed anymore. Expiry happens before a sale at the
    same timestamp.
    """
    @timeout(0.1)
    def test_02_expiry(self):
        inv = self.inventory
        inv.add_product(1, "lamp", 40)
        inv.restock(2, "lamp", 10)
        self.assertEqual(inv.reserve(3, "lamp", 4, 10), "res1")
        self.assertEqual(inv.get_stock(12, "lamp"), 6)
        self.assertEqual(inv.get_stock(13, "lamp"), 10)
        self.assertEqual(inv.confirm(14, "res1"), False)
        self.assertEqual(inv.reserve(15, "lamp", 10, 5), "res2")
        self.assertEqual(inv.sell(19, "lamp", 1), None)
        self.assertEqual(inv.sell(20, "lamp", 1), 9)
        self.assertEqual(inv.top_products(21, 1), ["lamp(40)"])

    """
    Confirming counts as a sale and works only once.
    Confirmed units never return; unconfirmed ones do.
    """
    @timeout(0.1)
    def test_03_confirm(self):
        inv = self.inventory
        inv.add_product(1, "book", 15)
        inv.add_product(2, "pen", 2)
        inv.restock(3, "book", 5)
        inv.restock(4, "pen", 50)
        self.assertEqual(inv.reserve(5, "book", 2, 100), "res1")
        self.assertEqual(inv.reserve(6, "pen", 10, 100), "res2")
        self.assertEqual(inv.confirm(7, "res1"), True)
        self.assertEqual(inv.confirm(8, "res1"), False)
        self.assertEqual(inv.confirm(9, "res9"), False)
        self.assertEqual(inv.get_stock(200, "book"), 3)
        self.assertEqual(inv.get_stock(201, "pen"), 50)
        self.assertEqual(inv.confirm(202, "res2"), False)
        self.assertEqual(inv.top_products(203, 2), ["book(30)", "pen(0)"])

    """
    low_stock sees reserved units as gone until they expire.
    """
    @timeout(0.1)
    def test_04_lowStockWithReservations(self):
        inv = self.inventory
        inv.add_product(1, "a", 10)
        inv.add_product(2, "b", 10)
        inv.restock(3, "a", 5)
        inv.restock(4, "b", 5)
        self.assertEqual(inv.reserve(5, "a", 4, 10), "res1")
        self.assertEqual(inv.low_stock(6, 3), ["a(1)"])
        self.assertEqual(inv.reserve(7, "b", 5, 20), "res2")
        self.assertEqual(inv.low_stock(8, 3), ["b(0)", "a(1)"])
        self.assertEqual(inv.low_stock(15, 3), ["b(0)"])
        self.assertEqual(inv.confirm(16, "res2"), True)
        self.assertEqual(inv.low_stock(30, 3), ["b(0)"])
        self.assertEqual(inv.get_stock(31, "a"), 5)
