import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from database import Database


class DatabaseLevel4Test(unittest.TestCase):
    """
    Graded tests for level 4. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.db = Database()

    """
    backup returns the number of live records at that moment.
    """
    @timeout(0.1)
    def test_01_backupCount(self):
        db = self.db
        self.assertEqual(db.backup(1), 0)
        db.set(2, "a", "x", "1")
        db.set(3, "b", "x", "2")
        db.set_with_ttl(4, "c", "x", "3", 10)
        self.assertEqual(db.backup(5), 3)
        self.assertEqual(db.backup(14), 2)
        self.assertEqual(db.delete(15, "a", "x"), True)
        self.assertEqual(db.backup(16), 1)

    """
    Backups at 2 ("one") and 4 ("two").
    restore(_, 3) picks the backup at 2; restore(_, 4) picks the one at 4.
    No backup at or before 1 -> False and nothing changes.
    """
    @timeout(0.1)
    def test_02_restoreLatestBackup(self):
        db = self.db
        db.set(1, "k", "v", "one")
        self.assertEqual(db.backup(2), 1)
        db.set(3, "k", "v", "two")
        self.assertEqual(db.backup(4), 1)
        db.set(5, "k", "v", "three")
        self.assertEqual(db.restore(6, 3), True)
        self.assertEqual(db.get(7, "k", "v"), "one")
        self.assertEqual(db.restore(8, 4), True)
        self.assertEqual(db.get(9, "k", "v"), "two")
        self.assertEqual(db.restore(10, 1), False)
        self.assertEqual(db.get(11, "k", "v"), "two")

    """
    Restore replaces the whole database: later records disappear,
    deleted ones come back.
    """
    @timeout(0.1)
    def test_03_restoreReplacesEverything(self):
        db = self.db
        db.set(1, "a", "f", "1")
        self.assertEqual(db.backup(2), 1)
        db.set(3, "b", "f", "2")
        self.assertEqual(db.delete(4, "a", "f"), True)
        self.assertEqual(db.restore(5, 2), True)
        self.assertEqual(db.get(6, "a", "f"), "1")
        self.assertEqual(db.get(7, "b", "f"), None)
        self.assertEqual(db.find(8, "f", "1"), ["a"])

    """
    token expires at 101; backed up at 11 with 90 left.
    Restored at 200 -> expires at 290.
    """
    @timeout(0.1)
    def test_04_restoreRecalculatesTtl(self):
        db = self.db
        db.set_with_ttl(1, "s", "tok", "x", 100)
        db.set(2, "s", "user", "ann")
        self.assertEqual(db.backup(11), 1)
        self.assertEqual(db.get(101, "s", "tok"), None)
        self.assertEqual(db.restore(200, 11), True)
        self.assertEqual(db.get_ttl(201, "s", "tok"), 89)
        self.assertEqual(db.get(289, "s", "tok"), "x")
        self.assertEqual(db.get(290, "s", "tok"), None)
        self.assertEqual(db.get(291, "s", "user"), "ann")

    """
    Fields expired at backup time aren't saved.
    The same backup can be restored twice.
    """
    @timeout(0.1)
    def test_05_expiredNotSavedAndRestoreTwice(self):
        db = self.db
        db.set_with_ttl(1, "a", "f", "1", 5)
        db.set(2, "b", "f", "2")
        self.assertEqual(db.backup(6), 1)
        self.assertEqual(db.restore(7, 6), True)
        self.assertEqual(db.get(8, "a", "f"), None)
        self.assertEqual(db.scan(9, "b", ""), ["f(2)"])
        db.set(10, "b", "g", "3")
        self.assertEqual(db.restore(11, 10), True)
        self.assertEqual(db.scan(12, "b", ""), ["f(2)"])
