import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from inventory import Inventory


class InventoryBasicTest(unittest.TestCase):
    """
    Playground: add your own tests here (e.g. the examples from each
    level's spec). These results are shown but don't count toward
    your score.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.inventory = Inventory()

    """
    Example from spec/level1.md
    """
    @timeout(0.1)
    def test_level1_example(self):
        inv = self.inventory
        self.assertEqual(inv.add_product(1, "apple", 50), True)
        self.assertEqual(inv.add_product(2, "apple", 70), False)
        self.assertEqual(inv.restock(3, "apple", 10), 10)
        self.assertEqual(inv.sell(4, "apple", 4), 6)
        self.assertEqual(inv.sell(5, "apple", 7), None)
        self.assertEqual(inv.get_stock(6, "apple"), 6)
        self.assertEqual(inv.get_stock(7, "banana"), None)
