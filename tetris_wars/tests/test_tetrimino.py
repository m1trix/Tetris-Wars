import unittest
from ..engine.tetrimino import *
from ..engine.grid import Grid, Rotation


class TestTetrimino(unittest.TestCase):

    def setUp(self):
        self.tetrimino = Tetrimino(
            Tetrimino.Type.L, 5, 5, [(0, 0), (0, 1), (1, 0)])

    def test_properties(self):
        self.assertEqual(self.tetrimino.size, 2)
        self.assertEqual(self.tetrimino.coords, (5, 5))
        self.assertEqual(self.tetrimino.measures, (2, 2))
        self.assertEqual(self.tetrimino.type, Tetrimino.Type.L)

        self.assertEqual(self.tetrimino.immutable().size, 2)
        self.assertEqual(self.tetrimino.immutable().coords, (5, 5))
        self.assertEqual(self.tetrimino.immutable().measures, (2, 2))
        self.assertEqual(self.tetrimino.immutable().type, Tetrimino.Type.L)

    def test_get_cell(self):
        self.assertIsNone(self.tetrimino.get_cell(4, 4))
        self.assertIsNone(self.tetrimino.get_cell(4, 5))
        self.assertIsNone(self.tetrimino.get_cell(5, 4))

        self.assertIsNone(self.tetrimino.immutable().get_cell(4, 4))
        self.assertIsNone(self.tetrimino.immutable().get_cell(4, 5))
        self.assertIsNone(self.tetrimino.immutable().get_cell(5, 4))

        self.assertIsNone(self.tetrimino.get_cell(6, 6))
        self.assertEqual(self.tetrimino.get_cell(5, 5).type, Tetrimino.Type.L)

        self.assertEqual(
            self.tetrimino.immutable().get_cell(5, 5).type, Tetrimino.Type.L)
        self.assertIsNone(self.tetrimino.immutable().get_cell(6, 6))

        self.assertIsNone(self.tetrimino.get_cell(7, 6))
        self.assertIsNone(self.tetrimino.get_cell(5, 7))
        self.assertIsNone(self.tetrimino.get_cell(7, 8))

        self.assertIsNone(self.tetrimino.immutable().get_cell(7, 6))
        self.assertIsNone(self.tetrimino.immutable().get_cell(5, 7))
        self.assertIsNone(self.tetrimino.immutable().get_cell(7, 8))

    def test_set_cell(self):
        self.tetrimino.set_cell(5, 5, True)
        self.tetrimino.set_cell(3, 3, True)         # No exceptions
        self.tetrimino.set_cell(100, 100, True)     # No exceptions
        self.assertEqual(self.tetrimino.get_cell(5, 5), True)

    def test_moving(self):
        self.tetrimino.move_relative(1, -1)
        self.assertEqual(self.tetrimino.coords, (6, 4))

        self.tetrimino.move_absolute(1, -1)
        self.assertEqual(self.tetrimino.coords, (1, -1))

    def test_iteration(self):
        segment = self.tetrimino.get_cell(5, 5)
        expected = [(5, 5, segment), (6, 5, segment), (5, 6, segment)]

        for actual in self.tetrimino:
            self.assertTrue(expected.count(actual) == 1)
        for actual in self.tetrimino.immutable():
            self.assertTrue(expected.count(actual) == 1)


class TestTetriminoUtils(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(4, 8)
        self.tetrimino = Tetrimino(
            Tetrimino.Type.L, 0, 0, [(0, 0), (0, 1), (1, 0)])

    def test_can_move(self):
        self.assertTrue(TetriminoUtils.can_move(
            self.tetrimino, self.grid, 0, 1))

        self.grid.set_cell(0, 2, True)
        self.assertFalse(TetriminoUtils.can_move(
            self.tetrimino, self.grid, 0, 1))

        self.tetrimino.move_absolute(0, 6)
        self.assertFalse(TetriminoUtils.can_move(
            self.tetrimino, self.grid, 0, 1))
        self.assertFalse(TetriminoUtils.can_move(
            self.tetrimino, self.grid, -1, 0))
        self.assertTrue(TetriminoUtils.can_move(
            self.tetrimino, self.grid, 1, 0))

        self.tetrimino.move_relative(2, 0)
        self.assertFalse(TetriminoUtils.can_move(
            self.tetrimino, self.grid, 0, 1))
        self.assertFalse(TetriminoUtils.can_move(
            self.tetrimino, self.grid, 1, 0))
        self.assertTrue(TetriminoUtils.can_move(
            self.tetrimino, self.grid, -1, 0))

    def test_rotate(self):
        TetriminoUtils.rotate(
            self.tetrimino, self.grid, Rotation.clockwise)      # xx xx
        self.assertEquals(self.tetrimino.coords, (0, 0))        # .. xx

        self.grid.set_cell(0, 1, True)
        TetriminoUtils.rotate(self.tetrimino, self.grid, Rotation.clockwise)
        self.assertEquals(self.tetrimino.coords, (0, -1))

    def test_calculate_actual_measures(self):
        tetrimino = Tetrimino(
            Tetrimino.Type.L, 0, 0, [(0, 0), (1, 1), (2, 1), (3, 3)])
        tetrimino.set_cell(0, 0, None)
        tetrimino.set_cell(3, 3, None)
        measures = TetriminoUtils.calculate_actual_measures(tetrimino)
        self.assertEqual(measures, (1, 1, 2, 1))
