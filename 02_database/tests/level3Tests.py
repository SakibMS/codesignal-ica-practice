import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from database import Database


class DatabaseLevel3Test(unittest.TestCase):
    """
    Graded tests for level 3. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.db = Database()

    """
    Field set at 1 with ttl 10 is visible until 10 and gone at 11.
    """
    @timeout(0.1)
    def test_01_expiry(self):
        db = self.db
        db.set_with_ttl(1, "sess", "token", "abc", 10)
        self.assertEqual(db.get(5, "sess", "token"), "abc")
        self.assertEqual(db.get(10, "sess", "token"), "abc")
        self.assertEqual(db.get(11, "sess", "token"), None)
        self.assertEqual(db.delete(12, "sess", "token"), False)
        self.assertEqual(db.scan(13, "sess", ""), [])

    """
    get_ttl: remaining time, -1 without TTL, None if missing or expired.
    """
    @timeout(0.1)
    def test_02_getTtl(self):
        db = self.db
        db.set(1, "k", "perm", "p")
        db.set_with_ttl(2, "k", "temp", "t", 100)
        self.assertEqual(db.get_ttl(3, "k", "perm"), -1)
        self.assertEqual(db.get_ttl(4, "k", "temp"), 98)
        self.assertEqual(db.get_ttl(5, "k", "nope"), None)
        self.assertEqual(db.get_ttl(102, "k", "temp"), None)
        self.assertEqual(db.get_ttl(103, "zzz", "temp"), None)

    """
    set removes a TTL; set_with_ttl replaces value and expiry.
    """
    @timeout(0.1)
    def test_03_overwriteTtl(self):
        db = self.db
        db.set_with_ttl(1, "k", "f", "v1", 10)
        db.set(5, "k", "f", "v2")
        self.assertEqual(db.get(20, "k", "f"), "v2")
        self.assertEqual(db.get_ttl(21, "k", "f"), -1)
        db.set_with_ttl(22, "k", "f", "v3", 5)
        self.assertEqual(db.get_ttl(23, "k", "f"), 4)
        db.set_with_ttl(24, "k", "f", "v4", 20)
        self.assertEqual(db.get(30, "k", "f"), "v4")
        self.assertEqual(db.get_ttl(31, "k", "f"), 13)
        self.assertEqual(db.get(44, "k", "f"), None)

    """
    scan, find and delete_record ignore expired fields.
    """
    @timeout(0.1)
    def test_04_expiredFieldsEverywhere(self):
        db = self.db
        db.set(1, "u1", "status", "online")
        db.set_with_ttl(2, "u2", "status", "online", 10)
        db.set_with_ttl(3, "u1", "badge", "gold", 5)
        self.assertEqual(db.scan(4, "u1", ""), ["badge(gold)", "status(online)"])
        self.assertEqual(db.find(5, "status", "online"), ["u1", "u2"])
        self.assertEqual(db.scan(8, "u1", ""), ["status(online)"])
        self.assertEqual(db.find(12, "status", "online"), ["u1"])
        db.set_with_ttl(13, "u3", "a", "1", 5)
        db.set_with_ttl(14, "u3", "b", "2", 10)
        db.set(15, "u3", "c", "3")
        self.assertEqual(db.delete_record(20, "u3"), 2)
        self.assertEqual(db.delete_record(21, "u2"), 0)
