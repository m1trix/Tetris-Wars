import unittest
from tetris_wars.engine.tetrimino import *


class TestTetriminoUtils(unittest.TestUtils):

    def setUp(self):
        self.grid = Grid(10, 20)

    def test_can_move(self):
        tetrimino = Tetrimino.create(Tetrimino.Type.L, (0, 5))
