import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from cloud_storage import CloudStorage


class CloudStorageLevel4Test(unittest.TestCase):
    """
    Graded tests for level 4. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.storage = CloudStorage()

    """
    Each update creates a new version.
    """
    @timeout(0.1)
    def test_01_updateAndVersion(self):
        fs = self.storage
        self.assertEqual(fs.add_file(1, "doc", 100), True)
        self.assertEqual(fs.get_version(2, "doc"), 1)
        self.assertEqual(fs.update_file(3, "doc", 150), 2)
        self.assertEqual(fs.update_file(4, "doc", 120), 3)
        self.assertEqual(fs.get_file_size(5, "doc"), 120)
        self.assertEqual(fs.get_version(6, "doc"), 3)
        self.assertEqual(fs.update_file(7, "nope", 10), None)
        self.assertEqual(fs.get_version(8, "nope"), None)

    """
    Versions: 1=10, 2=20, 3=30. Restoring creates new versions:
    4=10 (from 1), 5=30 (from 3), 6=10 (from 4).
    """
    @timeout(0.1)
    def test_02_restoreVersion(self):
        fs = self.storage
        self.assertEqual(fs.add_file(1, "cfg", 10), True)
        self.assertEqual(fs.update_file(2, "cfg", 20), 2)
        self.assertEqual(fs.update_file(3, "cfg", 30), 3)
        self.assertEqual(fs.restore_version(4, "cfg", 1), 4)
        self.assertEqual(fs.get_file_size(5, "cfg"), 10)
        self.assertEqual(fs.restore_version(6, "cfg", 3), 5)
        self.assertEqual(fs.get_file_size(7, "cfg"), 30)
        self.assertEqual(fs.restore_version(8, "cfg", 6), None)
        self.assertEqual(fs.restore_version(9, "cfg", 0), None)
        self.assertEqual(fs.restore_version(10, "x", 1), None)
        self.assertEqual(fs.restore_version(11, "cfg", 4), 6)
        self.assertEqual(fs.get_file_size(12, "cfg"), 10)

    """
    eve has 100. Only the current version counts toward her usage.
    Updates and restores that don't fit fail.
    """
    @timeout(0.1)
    def test_03_versionsAndCapacity(self):
        fs = self.storage
        self.assertEqual(fs.add_user(1, "eve", 100), True)
        self.assertEqual(fs.add_file_by(2, "eve", "/e/f", 50), 50)
        self.assertEqual(fs.update_file(3, "/e/f", 90), 2)
        self.assertEqual(fs.update_file(4, "/e/f", 101), None)
        self.assertEqual(fs.add_file_by(5, "eve", "/e/g", 10), 0)
        self.assertEqual(fs.restore_version(6, "/e/f", 1), 3)
        self.assertEqual(fs.add_file_by(7, "eve", "/e/h", 40), 0)
        self.assertEqual(fs.restore_version(8, "/e/f", 2), None)
        self.assertEqual(fs.get_version(9, "/e/f"), 3)
        self.assertEqual(fs.get_file_size(10, "/e/f"), 50)

    """
    A copy starts at version 1. Deleting a file deletes its history.
    """
    @timeout(0.1)
    def test_04_copyAndDeleteResetHistory(self):
        fs = self.storage
        self.assertEqual(fs.add_file(1, "a", 1), True)
        self.assertEqual(fs.update_file(2, "a", 2), 2)
        self.assertEqual(fs.update_file(3, "a", 3), 3)
        self.assertEqual(fs.copy_file(4, "a", "b"), True)
        self.assertEqual(fs.get_version(5, "b"), 1)
        self.assertEqual(fs.get_file_size(6, "b"), 3)
        self.assertEqual(fs.restore_version(7, "b", 2), None)
        self.assertEqual(fs.delete_file(8, "a"), 3)
        self.assertEqual(fs.add_file(9, "a", 7), True)
        self.assertEqual(fs.get_version(10, "a"), 1)
        self.assertEqual(fs.restore_version(11, "a", 2), None)

    """
    update_capacity uses current sizes: /m/a grew to 60, so it goes first.
    """
    @timeout(0.1)
    def test_05_updateCapacityUsesCurrentSize(self):
        fs = self.storage
        self.assertEqual(fs.add_user(1, "max", 100), True)
        self.assertEqual(fs.add_file_by(2, "max", "/m/a", 10), 90)
        self.assertEqual(fs.add_file_by(3, "max", "/m/b", 20), 70)
        self.assertEqual(fs.update_file(4, "/m/a", 60), 2)
        self.assertEqual(fs.update_capacity(5, "max", 50), 1)
        self.assertEqual(fs.get_version(6, "/m/a"), None)
        self.assertEqual(fs.find_files(7, "/m/", ""), ["/m/b(20)"])
