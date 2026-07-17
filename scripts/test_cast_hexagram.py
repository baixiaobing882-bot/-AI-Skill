#!/usr/bin/env python3
"""Self-contained tests for cast_hexagram.py."""

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("cast_hexagram.py")
SPEC = importlib.util.spec_from_file_location("cast_hexagram", MODULE_PATH)
CAST = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(CAST)


class CastTests(unittest.TestCase):
    def test_pure_qian_and_kun(self):
        self.assertEqual(CAST.hexagram([1] * 6)["number"], 1)
        self.assertEqual(CAST.hexagram([0] * 6)["number"], 2)

    def test_all_64_patterns_are_unique(self):
        numbers = set()
        for raw in range(64):
            bits = [(raw >> index) & 1 for index in range(6)]
            numbers.add(CAST.hexagram(bits)["number"])
        self.assertEqual(numbers, set(range(1, 65)))

    def test_coin_scoring(self):
        values, tosses = CAST.parse_coins(["TTT", "HTT", "HHT", "HHH", "TTT", "HTT"])
        self.assertEqual(values, [6, 7, 8, 9, 6, 7])
        self.assertEqual(tosses[0], "TTT")

    def test_moving_lines_flip(self):
        result = CAST.build_result("test", [6, 7, 8, 9, 7, 8], "test", None)
        self.assertEqual(result["moving_lines"], [1, 4])
        before = result["primary"]["bits_bottom_to_top"]
        after = result["changed"]["bits_bottom_to_top"]
        self.assertNotEqual(before[0], after[0])
        self.assertNotEqual(before[3], after[3])
        self.assertEqual(before[1:3], after[1:3])
        self.assertEqual(before[4:], after[4:])

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            CAST.build_result("bad", [7, 8, 9, 5, 7, 8], "test", None)


if __name__ == "__main__":
    unittest.main()
