import unittest
import utils.purge as purge
from utils.get_from_file import get_dict_data


class TestPurge(unittest.TestCase):
    def test_purge_wrong(self):
        words = get_dict_data()
        letters = "abcdefghijklmnop"
        correct = [
            "rurus", "rusts", "rutty", "sturt", "susus",
            "turrs", "tutty", "tutus", "usury", "vutty",
            "wurst", "wussy", "xysts", "yurts", "yuzus",
            "truss", "rusty", "tryst", "strut", "trust"
        ]
        self.assertEqual(purge.purge_wrong(letters, words), correct)

        words = ["hello", "peace", "treat"]
        letters = "a"
        correct = ["hello"]
        self.assertEqual(purge.purge_wrong(letters, words), correct)

    def test_purge_wrong_location(self):
        words = ["apple", "plant"]
        blocks = [('a', 0)]
        correct = ["plant"]
        self.assertEqual(purge.purge_wrong_location(blocks, words), correct)

    def test_blocks_to_list(self):
        blocks_str = "a1 b2 c3"
        correct = [('a', 0), ('b', 1), ('c', 2)]
        self.assertEqual(purge.blocks_to_list(blocks_str), correct)