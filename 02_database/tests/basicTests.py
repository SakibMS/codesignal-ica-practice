import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from database import Database


class DatabaseBasicTest(unittest.TestCase):
    """
    Playground: add your own tests here (e.g. the examples from each
    level's spec). These results are shown but don't count toward
    your score.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.db = Database()

    """
    Example from spec/level1.md
    """
    @timeout(0.1)
    def test_level1_example(self):
        db = self.db
        db.set(1, "user1", "name", "Ada")
        db.set(2, "user1", "city", "Paris")
        self.assertEqual(db.get(3, "user1", "name"), "Ada")
        self.assertEqual(db.get(4, "user1", "age"), None)
        self.assertEqual(db.delete(5, "user1", "city"), True)
        self.assertEqual(db.delete(6, "user1", "city"), False)
        self.assertEqual(db.delete_record(7, "user1"), 1)
        self.assertEqual(db.get(8, "user1", "name"), None)
