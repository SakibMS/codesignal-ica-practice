import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from cloud_storage import CloudStorage


class CloudStorageLevel1Test(unittest.TestCase):
    """
    Graded tests for level 1. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.storage = CloudStorage()

    """
    Add two files; a duplicate name fails.
    """
    @timeout(0.1)
    def test_01_addAndGet(self):
        fs = self.storage
        self.assertEqual(fs.add_file(1, "/docs/a.txt", 100), True)
        self.assertEqual(fs.add_file(2, "/docs/a.txt", 200), False)
        self.assertEqual(fs.add_file(3, "/img/b.png", 300), True)
        self.assertEqual(fs.get_file_size(4, "/docs/a.txt"), 100)
        self.assertEqual(fs.get_file_size(5, "/img/b.png"), 300)
        self.assertEqual(fs.get_file_size(6, "/none"), None)

    """
    delete_file returns the size; the name can be reused afterwards.
    """
    @timeout(0.1)
    def test_02_delete(self):
        fs = self.storage
        self.assertEqual(fs.add_file(1, "f1", 10), True)
        self.assertEqual(fs.delete_file(2, "f1"), 10)
        self.assertEqual(fs.delete_file(3, "f1"), None)
        self.assertEqual(fs.get_file_size(4, "f1"), None)
        self.assertEqual(fs.add_file(5, "f1", 20), True)
        self.assertEqual(fs.get_file_size(6, "f1"), 20)

    """
    Copy needs an existing source and a free destination.
    The copy survives deleting the original.
    """
    @timeout(0.1)
    def test_03_copy(self):
        fs = self.storage
        self.assertEqual(fs.add_file(1, "a", 5), True)
        self.assertEqual(fs.add_file(2, "b", 7), True)
        self.assertEqual(fs.copy_file(3, "a", "c"), True)
        self.assertEqual(fs.get_file_size(4, "c"), 5)
        self.assertEqual(fs.copy_file(5, "a", "b"), False)
        self.assertEqual(fs.copy_file(6, "x", "y"), False)
        self.assertEqual(fs.get_file_size(7, "y"), None)
        self.assertEqual(fs.get_file_size(8, "b"), 7)
        self.assertEqual(fs.delete_file(9, "a"), 5)
        self.assertEqual(fs.get_file_size(10, "c"), 5)
        self.assertEqual(fs.copy_file(11, "c", "a"), True)
        self.assertEqual(fs.get_file_size(12, "a"), 5)
