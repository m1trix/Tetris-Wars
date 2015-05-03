import unittest
from tetris_wars.engine.grid import *


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(4, 8)

    def test_initialize(self):
        w, h = self.grid.measures
        self.assertEqual(w, 4)
        self.assertEqual(h, 8)

        for y in range(8):
            for x in range(4):
                self.assertFalse(self.grid.get_cell((x, y)))

    def test_cell_modification(self):
        self.grid.set_cell((0, 0), True)
        self.grid.set_cell((3, 4), True)

        self.assertTrue(self.grid.get_cell((0, 0)))
        self.assertTrue(self.grid.get_cell((3, 4)))

        self.grid.set_cell((0, 0), False)
        self.assertFalse(self.grid.get_cell((0, 0)))


class TestSpinGrid(unittest.TestCase):

    def setUp(self):
        self.grid = SpinGrid([(3, 3)])

    def test_initialization(self):
        w, h = self.grid.measures
        self.assertEqual(w, 4)
        self.assertEqual(h, 4)
        self.assertTrue(self.grid.get_cell((3, 3)))

    def test_rotation(self):
        self.grid.rotate(Rotation.clockwise)
        self.assertFalse(self.grid.get_cell((3, 3)))
        self.assertTrue(self.grid.get_cell((0, 3)))

        self.grid.rotate(Rotation.clockwise)
        self.assertFalse(self.grid.get_cell((0, 3)))
        self.assertTrue(self.grid.get_cell((0, 0)))

        self.grid.rotate(Rotation.clockwise)
        self.assertFalse(self.grid.get_cell((0, 0)))
        self.assertTrue(self.grid.get_cell((3, 0)))

        self.grid.rotate(Rotation.clockwise)
        self.assertFalse(self.grid.get_cell((3, 0)))
        self.assertTrue(self.grid.get_cell((3, 3)))

    def test_inverse_rotation(self):
        self.grid.rotate(Rotation.counterclockwise)
        self.assertFalse(self.grid.get_cell((3, 3)))
        self.assertTrue(self.grid.get_cell((3, 0)))

        self.grid.rotate(Rotation.counterclockwise)
        self.assertFalse(self.grid.get_cell((3, 0)))
        self.assertTrue(self.grid.get_cell((0, 0)))

        self.grid.rotate(Rotation.counterclockwise)
        self.assertFalse(self.grid.get_cell((0, 0)))
        self.assertTrue(self.grid.get_cell((0, 3)))

        self.grid.rotate(Rotation.counterclockwise)
        self.assertFalse(self.grid.get_cell((0, 3)))
        self.assertTrue(self.grid.get_cell((3, 3)))

    def test_set_cell(self):
        self.grid.set_cell((0, 0), True)
        self.assertTrue(self.grid.get_cell((0, 0)))

        self.grid.set_cell((0, 0), False)
        self.assertFalse(self.grid.get_cell((0, 0)))

        self.grid.rotate(Rotation.clockwise)
        self.grid.set_cell((0, 0), True)

        self.grid.rotate(Rotation.clockwise)
        self.assertTrue(self.grid.get_cell((3, 0)))

    def test_invalid_rotation(self):
        with self.assertRaises(RotationError):
            self.grid.rotate("arround")