import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from inventory import Inventory


class InventoryLevel2Test(unittest.TestCase):
    """
    Graded tests for level 2. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.inventory = Inventory()

    """
    tea: 5 x 300 = 1500, coffee: 3 x 500 = 1500, juice: 2 x 250 = 500
    Ties are broken by product id.
    Then juice sells 8 more -> 2500.
    """
    @timeout(0.1)
    def test_01_topProducts(self):
        inv = self.inventory
        inv.add_product(1, "tea", 300)
        inv.add_product(2, "coffee", 500)
        inv.add_product(3, "juice", 250)
        inv.restock(4, "tea", 10)
        inv.restock(5, "coffee", 10)
        inv.restock(6, "juice", 10)
        self.assertEqual(inv.sell(7, "tea", 5), 5)
        self.assertEqual(inv.sell(8, "coffee", 3), 7)
        self.assertEqual(inv.sell(9, "juice", 2), 8)
        self.assertEqual(inv.top_products(10, 2), ["coffee(1500)", "tea(1500)"])
        self.assertEqual(
            inv.top_products(11, 5),
            ["coffee(1500)", "tea(1500)", "juice(500)"]
        )
        self.assertEqual(inv.sell(12, "juice", 8), 0)
        self.assertEqual(inv.top_products(13, 1), ["juice(2500)"])

    """
    Products without sales are listed with revenue 0.
    A failed sale earns nothing.
    """
    @timeout(0.1)
    def test_02_zeroRevenueAndFailedSales(self):
        inv = self.inventory
        inv.add_product(1, "x", 100)
        inv.add_product(2, "y", 100)
        inv.add_product(3, "w", 100)
        self.assertEqual(inv.top_products(4, 3), ["w(0)", "x(0)", "y(0)"])
        inv.restock(5, "y", 1)
        self.assertEqual(inv.sell(6, "y", 2), None)
        self.assertEqual(inv.sell(7, "y", 1), 0)
        self.assertEqual(inv.top_products(8, 2), ["y(100)", "w(0)"])

    """
    Stock strictly below the threshold, sorted by stock, then id.
    """
    @timeout(0.1)
    def test_03_lowStock(self):
        inv = self.inventory
        inv.add_product(1, "bolt", 5)
        inv.add_product(2, "nut", 3)
        inv.add_product(3, "screw", 4)
        inv.add_product(4, "washer", 1)
        inv.restock(5, "bolt", 20)
        inv.restock(6, "nut", 4)
        inv.restock(7, "screw", 4)
        self.assertEqual(inv.low_stock(8, 5), ["washer(0)", "nut(4)", "screw(4)"])
        self.assertEqual(inv.low_stock(9, 4), ["washer(0)"])
        self.assertEqual(inv.low_stock(10, 0), [])
        self.assertEqual(inv.sell(11, "bolt", 17), 3)
        self.assertEqual(inv.low_stock(12, 4), ["washer(0)", "bolt(3)"])
        self.assertEqual(
            inv.low_stock(13, 100),
            ["washer(0)", "bolt(3)", "nut(4)", "screw(4)"]
        )
