import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from database import Database


class DatabaseLevel2Test(unittest.TestCase):
    """
    Graded tests for level 2. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.db = Database()

    """
    Empty prefix lists every field, sorted by field name.
    """
    @timeout(0.1)
    def test_01_scanAll(self):
        db = self.db
        db.set(1, "cfg", "timeout", "30")
        db.set(2, "cfg", "retries", "5")
        db.set(3, "cfg", "mode", "fast")
        self.assertEqual(
            db.scan(4, "cfg", ""),
            ["mode(fast)", "retries(5)", "timeout(30)"]
        )
        self.assertEqual(db.scan(5, "missing", ""), [])
        db.set(6, "cfg", "mode", "safe")
        self.assertEqual(
            db.scan(7, "cfg", ""),
            ["mode(safe)", "retries(5)", "timeout(30)"]
        )

    """
    Only fields starting with the prefix.
    """
    @timeout(0.1)
    def test_02_scanPrefix(self):
        db = self.db
        db.set(1, "app", "db_host", "localhost")
        db.set(2, "app", "db_port", "5432")
        db.set(3, "app", "debug", "true")
        db.set(4, "app", "cache", "on")
        self.assertEqual(
            db.scan(5, "app", "db"),
            ["db_host(localhost)", "db_port(5432)"]
        )
        self.assertEqual(
            db.scan(6, "app", "d"),
            ["db_host(localhost)", "db_port(5432)", "debug(true)"]
        )
        self.assertEqual(db.scan(7, "app", "x"), [])
        self.assertEqual(db.delete(8, "app", "db_host"), True)
        self.assertEqual(db.scan(9, "app", "db_"), ["db_port(5432)"])

    """
    find returns matching keys in sorted order and reflects updates.
    """
    @timeout(0.1)
    def test_03_find(self):
        db = self.db
        db.set(1, "zoe", "team", "red")
        db.set(2, "max", "team", "blue")
        db.set(3, "amy", "team", "red")
        db.set(4, "kim", "role", "red")
        self.assertEqual(db.find(5, "team", "red"), ["amy", "zoe"])
        self.assertEqual(db.find(6, "team", "green"), [])
        self.assertEqual(db.find(7, "role", "red"), ["kim"])
        db.set(8, "max", "team", "red")
        self.assertEqual(db.delete_record(9, "zoe"), 1)
        self.assertEqual(db.find(10, "team", "red"), ["amy", "max"])
