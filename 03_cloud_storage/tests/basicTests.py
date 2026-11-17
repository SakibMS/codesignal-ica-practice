import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from cloud_storage import CloudStorage


class CloudStorageBasicTest(unittest.TestCase):
    """
    Playground: add your own tests here (e.g. the examples from each
    level's spec). These results are shown but don't count toward
    your score.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.storage = CloudStorage()

    """
    Example from spec/level1.md
    """
    @timeout(0.1)
    def test_level1_example(self):
        fs = self.storage
        self.assertEqual(fs.add_file(1, "/docs/cv.pdf", 200), True)
        self.assertEqual(fs.add_file(2, "/docs/cv.pdf", 300), False)
        self.assertEqual(fs.copy_file(3, "/docs/cv.pdf", "/backup/cv.pdf"), True)
        self.assertEqual(fs.get_file_size(4, "/backup/cv.pdf"), 200)
        self.assertEqual(fs.delete_file(5, "/docs/cv.pdf"), 200)
        self.assertEqual(fs.get_file_size(6, "/docs/cv.pdf"), None)
