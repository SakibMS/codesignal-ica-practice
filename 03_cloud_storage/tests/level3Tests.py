import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from cloud_storage import CloudStorage


class CloudStorageLevel3Test(unittest.TestCase):
    """
    Graded tests for level 3. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.storage = CloudStorage()

    """
    u1 has 1000: 300 + 700 fills it exactly.
    Deleting a file frees space.
    """
    @timeout(0.1)
    def test_01_userCapacity(self):
        fs = self.storage
        self.assertEqual(fs.add_user(1, "u1", 1000), True)
        self.assertEqual(fs.add_user(2, "u1", 500), False)
        self.assertEqual(fs.add_file_by(3, "u1", "/u1/a", 300), 700)
        self.assertEqual(fs.add_file_by(4, "u1", "/u1/b", 700), 0)
        self.assertEqual(fs.add_file_by(5, "u1", "/u1/c", 1), None)
        self.assertEqual(fs.add_file_by(6, "u2", "/u2/a", 1), None)
        self.assertEqual(fs.add_user(7, "u2", 100), True)
        self.assertEqual(fs.add_file_by(8, "u2", "/u1/a", 5), None)
        self.assertEqual(fs.delete_file(9, "/u1/b"), 700)
        self.assertEqual(fs.add_file_by(10, "u1", "/u1/c", 500), 200)
        self.assertEqual(fs.get_file_size(11, "/u1/c"), 500)

    """
    Admin files have no limit. A copy is owned by the source's owner
    and must fit in their capacity.
    """
    @timeout(0.1)
    def test_02_adminAndCopyOwnership(self):
        fs = self.storage
        self.assertEqual(fs.add_user(1, "bob", 100), True)
        self.assertEqual(fs.add_file(2, "/shared/big", 10 ** 6), True)
        self.assertEqual(fs.copy_file(3, "/shared/big", "/shared/big2"), True)
        self.assertEqual(fs.add_file_by(4, "bob", "/bob/a", 60), 40)
        self.assertEqual(fs.copy_file(5, "/bob/a", "/bob/a_copy"), False)
        self.assertEqual(fs.add_file_by(6, "bob", "/bob/b", 30), 10)
        self.assertEqual(fs.delete_file(7, "/bob/a"), 60)
        self.assertEqual(fs.copy_file(8, "/bob/b", "/bob/b_copy"), True)
        self.assertEqual(fs.add_file_by(9, "bob", "/bob/c", 41), None)
        self.assertEqual(fs.add_file_by(10, "bob", "/bob/c", 40), 0)

    """
    amy uses 1000 (400 + 300 + 200 + 100).
    Capacity 700 -> delete 400 (1 file). Capacity 250 -> delete 300, 200 (2 files).
    """
    @timeout(0.1)
    def test_03_updateCapacity(self):
        fs = self.storage
        self.assertEqual(fs.add_user(1, "amy", 1000), True)
        self.assertEqual(fs.add_file_by(2, "amy", "/a/1", 400), 600)
        self.assertEqual(fs.add_file_by(3, "amy", "/a/2", 300), 300)
        self.assertEqual(fs.add_file_by(4, "amy", "/a/3", 200), 100)
        self.assertEqual(fs.add_file_by(5, "amy", "/a/4", 100), 0)
        self.assertEqual(fs.update_capacity(6, "amy", 700), 1)
        self.assertEqual(fs.get_file_size(7, "/a/1"), None)
        self.assertEqual(fs.update_capacity(8, "amy", 250), 2)
        self.assertEqual(fs.find_files(9, "/a/", ""), ["/a/4(100)"])
        self.assertEqual(fs.update_capacity(10, "amy", 5000), 0)
        self.assertEqual(fs.add_file_by(11, "amy", "/a/5", 4900), 0)
        self.assertEqual(fs.update_capacity(12, "zed", 10), None)

    """
    Equal sizes are deleted in name order. Other owners' files are untouched.
    """
    @timeout(0.1)
    def test_04_updateCapacityTies(self):
        fs = self.storage
        self.assertEqual(fs.add_user(1, "kai", 100), True)
        self.assertEqual(fs.add_file_by(2, "kai", "/k/b", 30), 70)
        self.assertEqual(fs.add_file_by(3, "kai", "/k/a", 30), 40)
        self.assertEqual(fs.add_file_by(4, "kai", "/k/c", 30), 10)
        self.assertEqual(fs.add_file(5, "/k/admin", 999), True)
        self.assertEqual(fs.update_capacity(6, "kai", 40), 2)
        self.assertEqual(fs.find_files(7, "/k/", ""), ["/k/admin(999)", "/k/c(30)"])
