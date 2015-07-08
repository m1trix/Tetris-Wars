import unittest
from ..engine.grid import *


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(4, 8)

    def test_initialize(self):
        w, h = self.grid.measures
        self.assertEqual(w, 4)
        self.assertEqual(h, 8)

        for y in range(8):
            for x in range(4):
                self.assertIsNone(self.grid.get_cell(x, y))

    def test_cell_modification(self):
        self.grid.set_cell(0, 0, True)
        self.grid.set_cell(3, 4, True)

        self.assertTrue(self.grid.get_cell(0, 0))
        self.assertTrue(self.grid.get_cell(3, 4))

        self.grid.set_cell(0, 0, False)
        self.assertFalse(self.grid.get_cell(0, 0))

    def test_immutable(self):
        self.assertIsInstance(self.grid.immutable(), ImmutableGrid)


class TestImmutableGrid(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(4, 8)
        self.immutable_grid = ImmutableGrid(self.grid)

    def test_measures(self):
        self.assertEqual(self.immutable_grid.measures, (4, 8))

    def test_get_cell(self):
        self.grid.set_cell(1, 1, 42)
        self.grid.set_cell(3, 3, "String")
        self.assertEqual(self.immutable_grid.get_cell(1, 1), 42)
        self.assertEqual(self.immutable_grid.get_cell(3, 3), "String")

    def test_get_row(self):
        self.grid.set_cell(1, 1, 42)
        expected = (None, 42, None, None)
        for x in range(4):
            self.assertEqual(self.immutable_grid.get_cell(x, 1), expected[x])


class TestSpinGrid(unittest.TestCase):

    def setUp(self):
        self.grid = RotatableGrid([(1, 0), (1, 1), (0, 1)], True)

    def test_measures(self):
        grid = RotatableGrid([(3, 4)], True)
        self.assertEqual(grid.measures, (5, 5))

    def test_clockwise_rotation(self):
        self.grid.rotate(Rotation.clockwise)
        self.assertEqual(self.grid.get_cell(0, 0), True)
        self.assertEqual(self.grid.get_cell(0, 1), True)
        self.assertEqual(self.grid.get_cell(1, 0), None)
        self.assertEqual(self.grid.get_cell(1, 1), True)

        self.grid.rotate(Rotation.clockwise)
        self.assertEqual(self.grid.get_cell(0, 0), True)
        self.assertEqual(self.grid.get_cell(0, 1), True)
        self.assertEqual(self.grid.get_cell(1, 0), True)
        self.assertEqual(self.grid.get_cell(1, 1), None)

        self.grid.rotate(Rotation.clockwise)
        self.assertEqual(self.grid.get_cell(0, 0), True)
        self.assertEqual(self.grid.get_cell(0, 1), None)
        self.assertEqual(self.grid.get_cell(1, 0), True)
        self.assertEqual(self.grid.get_cell(1, 1), True)

        self.grid.rotate(Rotation.clockwise)
        self.assertEqual(self.grid.get_cell(0, 0), None)
        self.assertEqual(self.grid.get_cell(0, 1), True)
        self.assertEqual(self.grid.get_cell(1, 0), True)
        self.assertEqual(self.grid.get_cell(1, 1), True)

    def test_counterclockwise_rotation(self):
        self.grid.rotate(Rotation.counterclockwise)
        self.assertEqual(self.grid.get_cell(0, 0), True)
        self.assertEqual(self.grid.get_cell(0, 1), None)
        self.assertEqual(self.grid.get_cell(1, 0), True)
        self.assertEqual(self.grid.get_cell(1, 1), True)

        self.grid.rotate(Rotation.counterclockwise)
        self.assertEqual(self.grid.get_cell(0, 0), True)
        self.assertEqual(self.grid.get_cell(0, 1), True)
        self.assertEqual(self.grid.get_cell(1, 0), True)
        self.assertEqual(self.grid.get_cell(1, 1), None)

        self.grid.rotate(Rotation.counterclockwise)
        self.assertEqual(self.grid.get_cell(0, 0), True)
        self.assertEqual(self.grid.get_cell(0, 1), True)
        self.assertEqual(self.grid.get_cell(1, 0), None)
        self.assertEqual(self.grid.get_cell(1, 1), True)

        self.grid.rotate(Rotation.counterclockwise)
        self.assertEqual(self.grid.get_cell(0, 0), None)
        self.assertEqual(self.grid.get_cell(0, 1), True)
        self.assertEqual(self.grid.get_cell(1, 0), True)
        self.assertEqual(self.grid.get_cell(1, 1), True)

    def test_invalid_rotation(self):
        with self.assertRaises(RotationError):
            self.grid.rotate('invalid')

    def test_set_cell(self):
        self.grid.rotate(Rotation.clockwise)
        self.grid.rotate(Rotation.clockwise)
        self.grid.set_cell(1, 1, 'Non-Null')

        self.grid.rotate(Rotation.clockwise)
        self.grid.rotate(Rotation.clockwise)
        self.assertEqual(self.grid.get_cell(0, 0), 'Non-Null')


class TestGridUtils(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(4, 8)

    def fill_lines(self, lines, value):
        for y in lines:
            for x in range(4):
                self.grid.set_cell(x, y, value)

    def assert_line(self, y, expected):
        for x in range(4):
            self.assertEqual(self.grid.get_cell(x, y), expected[x])

    def test_get_full_lines(self):
        self.assertEqual(GridUtils.get_full_lines(self.grid), [])
        expected_lines = [0, 2, 4, 6]
        self.fill_lines(expected_lines, True)
        actual_lines = GridUtils.get_full_lines(self.grid)
        self.assertEqual(actual_lines, expected_lines)

    def test_clear_lines(self):
        self.fill_lines([0, 1], True)
        self.grid.set_cell(1, 1, None)

        GridUtils.clear_lines(self.grid, [0])
        self.assert_line(0, [None] * 4)
        self.assert_line(1, [True, None, True, True])

    def test_remove_lines(self):
        self.fill_lines([0, 1], True)
        self.grid.set_cell(0, 0, None)
        GridUtils.remove_lines(self.grid, [1])
        self.assert_line(0, [None] * 4)
        self.assert_line(1, [None] + [True] * 3)
