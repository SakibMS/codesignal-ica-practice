import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from cloud_storage import CloudStorage


class CloudStorageLevel2Test(unittest.TestCase):
    """
    Graded tests for level 2. Read them if you like, but don't edit them.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.storage = CloudStorage()

    """
    Matches on prefix AND suffix, sorted by size desc, then name.
    """
    @timeout(0.1)
    def test_01_findFiles(self):
        fs = self.storage
        fs.add_file(1, "/music/song1.mp3", 300)
        fs.add_file(2, "/music/song2.mp3", 500)
        fs.add_file(3, "/music/notes.txt", 10)
        fs.add_file(4, "/music/song3.mp3", 300)
        fs.add_file(5, "/video/clip.mp4", 900)
        self.assertEqual(
            fs.find_files(6, "/music/", ".mp3"),
            ["/music/song2.mp3(500)", "/music/song1.mp3(300)", "/music/song3.mp3(300)"]
        )
        self.assertEqual(fs.find_files(7, "/music/", ".txt"), ["/music/notes.txt(10)"])
        self.assertEqual(fs.find_files(8, "/video", ".mp3"), [])
        self.assertEqual(
            fs.find_files(9, "/", ""),
            [
                "/video/clip.mp4(900)", "/music/song2.mp3(500)",
                "/music/song1.mp3(300)", "/music/song3.mp3(300)",
                "/music/notes.txt(10)",
            ]
        )

    """
    12 logs: /logs/log00.txt (100) ... /logs/log11.txt (111).
    Only the 10 largest are returned.
    """
    @timeout(0.1)
    def test_02_atMostTenResults(self):
        fs = self.storage
        for i in range(12):
            fs.add_file(i + 1, f"/logs/log{i:02d}.txt", 100 + i)
        self.assertEqual(
            fs.find_files(13, "/logs/", ".txt"),
            [f"/logs/log{i:02d}.txt({100 + i})" for i in range(11, 1, -1)]
        )
        self.assertEqual(fs.delete_file(14, "/logs/log11.txt"), 111)
        self.assertEqual(
            fs.find_files(15, "/logs/log0", ".txt"),
            [f"/logs/log{i:02d}.txt({100 + i})" for i in range(9, -1, -1)]
        )

    """
    total_size sums every file whose name starts with the prefix.
    """
    @timeout(0.1)
    def test_03_totalSize(self):
        fs = self.storage
        fs.add_file(1, "/a/x", 10)
        fs.add_file(2, "/a/y", 20)
        fs.add_file(3, "/ab/z", 40)
        fs.add_file(4, "/b/w", 80)
        self.assertEqual(fs.total_size(5, "/a/"), 30)
        self.assertEqual(fs.total_size(6, "/a"), 70)
        self.assertEqual(fs.total_size(7, "/"), 150)
        self.assertEqual(fs.total_size(8, "/c"), 0)
        self.assertEqual(fs.delete_file(9, "/a/x"), 10)
        self.assertEqual(fs.copy_file(10, "/b/w", "/a/w"), True)
        self.assertEqual(fs.total_size(11, "/a/"), 100)
