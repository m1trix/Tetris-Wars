import unittest
from ..engine.utils import *


class TestEngineUtils(unittest.TestCase):

    def test_tuple_add(self):
        self.assertEqual(tuple_add((1, 2), (3, 4)), (4, 6))
        with self.assertRaises(Exception):
            tuple_add((1,), (1, 2))

    def test_tuple_sub(self):
        self.assertEqual(tuple_sub((1, 2), (3, 4)), (-2, -2))
        with self.assertRaises(Exception):
            tuple_sub((1,), (1, 2))
