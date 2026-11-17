import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from database import Database


class DatabaseLevel1Test(unittest.TestCase):
    """
    Graded tests for level 1. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.db = Database()

    """
    Set two fields, read them back, overwrite one.
    Missing records and fields -> None.
    """
    @timeout(0.1)
    def test_01_setAndGet(self):
        db = self.db
        db.set(1, "user1", "name", "Ada")
        db.set(2, "user1", "city", "London")
        self.assertEqual(db.get(3, "user1", "name"), "Ada")
        self.assertEqual(db.get(4, "user1", "age"), None)
        self.assertEqual(db.get(5, "user2", "name"), None)
        db.set(6, "user1", "name", "Grace")
        self.assertEqual(db.get(7, "user1", "name"), "Grace")
        self.assertEqual(db.get(8, "user1", "city"), "London")

    """
    Delete returns True only when the field existed.
    """
    @timeout(0.1)
    def test_02_delete(self):
        db = self.db
        db.set(1, "k", "a", "1")
        db.set(2, "k", "b", "2")
        self.assertEqual(db.delete(3, "k", "a"), True)
        self.assertEqual(db.delete(4, "k", "a"), False)
        self.assertEqual(db.get(5, "k", "a"), None)
        self.assertEqual(db.get(6, "k", "b"), "2")
        self.assertEqual(db.delete(7, "x", "a"), False)
        self.assertEqual(db.delete(8, "k", "b"), True)
        self.assertEqual(db.get(9, "k", "b"), None)

    """
    delete_record returns the number of fields removed.
    A record whose last field was deleted no longer exists.
    """
    @timeout(0.1)
    def test_03_deleteRecord(self):
        db = self.db
        db.set(1, "r1", "f1", "v1")
        db.set(2, "r1", "f2", "v2")
        db.set(3, "r1", "f3", "v3")
        db.set(4, "r2", "f1", "v1")
        self.assertEqual(db.delete_record(5, "r1"), 3)
        self.assertEqual(db.delete_record(6, "r1"), 0)
        self.assertEqual(db.get(7, "r1", "f1"), None)
        self.assertEqual(db.get(8, "r2", "f1"), "v1")
        self.assertEqual(db.delete(9, "r2", "f1"), True)
        self.assertEqual(db.delete_record(10, "r2"), 0)
        db.set(11, "r1", "f9", "new")
        self.assertEqual(db.delete_record(12, "r1"), 1)
