import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from inventory import Inventory


class InventoryLevel4Test(unittest.TestCase):
    """
    Graded tests for level 4. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.inventory = Inventory()

    """
    2 x 200 = 400, then price -> 250, 2 x 250 = 500. Total 900.
    """
    @timeout(0.1)
    def test_01_setPrice(self):
        inv = self.inventory
        inv.add_product(1, "milk", 200)
        inv.restock(2, "milk", 10)
        self.assertEqual(inv.sell(3, "milk", 2), 8)
        self.assertEqual(inv.set_price(4, "milk", 250), True)
        self.assertEqual(inv.set_price(5, "bread", 100), False)
        self.assertEqual(inv.sell(6, "milk", 2), 6)
        self.assertEqual(inv.top_products(7, 1), ["milk(900)"])

    """
    Sales: 100 at t=10, 200 at t=20, 450 at t=30 (after a price change).
    Ranges are inclusive on both ends.
    """
    @timeout(0.1)
    def test_02_revenueInRange(self):
        inv = self.inventory
        inv.add_product(1, "gum", 100)
        inv.restock(2, "gum", 100)
        self.assertEqual(inv.sell(10, "gum", 1), 99)
        self.assertEqual(inv.sell(20, "gum", 2), 97)
        self.assertEqual(inv.set_price(25, "gum", 150), True)
        self.assertEqual(inv.sell(30, "gum", 3), 94)
        self.assertEqual(inv.get_revenue(40, "gum", 10, 30), 750)
        self.assertEqual(inv.get_revenue(41, "gum", 11, 29), 200)
        self.assertEqual(inv.get_revenue(42, "gum", 20, 20), 200)
        self.assertEqual(inv.get_revenue(43, "gum", 31, 43), 0)
        self.assertEqual(inv.get_revenue(44, "candy", 0, 44), None)
        self.assertEqual(inv.get_revenue(45, "gum", 0, 5), 0)

    """
    res1 locks 2 shoes at 1000; the price then rises to 1200.
    res2 locks 1 shoe at 1200 and is confirmed at t=6; 1 shoe sold at t=7.
    res1 is confirmed at t=50 and charged the locked 2 x 1000.
    """
    @timeout(0.1)
    def test_03_reservationLocksPrice(self):
        inv = self.inventory
        inv.add_product(1, "shoe", 1000)
        inv.restock(2, "shoe", 10)
        self.assertEqual(inv.reserve(3, "shoe", 2, 100), "res1")
        self.assertEqual(inv.set_price(4, "shoe", 1200), True)
        self.assertEqual(inv.reserve(5, "shoe", 1, 100), "res2")
        self.assertEqual(inv.confirm(6, "res2"), True)
        self.assertEqual(inv.sell(7, "shoe", 1), 6)
        self.assertEqual(inv.confirm(50, "res1"), True)
        self.assertEqual(inv.get_revenue(60, "shoe", 0, 10), 2400)
        self.assertEqual(inv.get_revenue(61, "shoe", 50, 50), 2000)
        self.assertEqual(inv.top_products(62, 1), ["shoe(4400)"])

    """
    An expired reservation earns nothing; the units are later sold
    at the new price (5 x 35 = 175).
    """
    @timeout(0.1)
    def test_04_expiredReservationEarnsNothing(self):
        inv = self.inventory
        inv.add_product(1, "cap", 30)
        inv.add_product(2, "hat", 40)
        inv.restock(3, "cap", 5)
        inv.restock(4, "hat", 5)
        self.assertEqual(inv.reserve(5, "cap", 5, 10), "res1")
        self.assertEqual(inv.set_price(6, "cap", 35), True)
        self.assertEqual(inv.sell(7, "hat", 5), 0)
        self.assertEqual(inv.confirm(15, "res1"), False)
        self.assertEqual(inv.sell(16, "cap", 5), 0)
        self.assertEqual(inv.get_revenue(17, "cap", 0, 17), 175)
        self.assertEqual(inv.get_revenue(18, "hat", 7, 7), 200)
        self.assertEqual(inv.top_products(19, 2), ["hat(200)", "cap(175)"])
        self.assertEqual(inv.low_stock(20, 1), ["cap(0)", "hat(0)"])
