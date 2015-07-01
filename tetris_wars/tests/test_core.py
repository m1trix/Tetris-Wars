import unittest
from engine.utils import *
from engine.grid import *
from engine.tetrimino import *
from engine.core import GameCore
from engine.settings import Settings


class TestCore(unittest.TestCase):

    def setUp(self):
        self.core = GameCore(Settings())

    def test_init(self):
        self.assertIsNotNone(self.core.tetrimino)
        self.assertIsNotNone(self.core.tetrimino_ghost)

    def test_refresh_ghost_tetrimino(self):
        self.assertEqual(self.core.tetrimino.coords[0],
                         self.core.tetrimino_ghost.coords[0])

        self.core.tetrimino.move_relative((1, 0))
        self.assertEqual(self.core.tetrimino.coords[0] - 1,
                         self.core.tetrimino_ghost.coords[0])

        self.core.refresh_ghost_tetrimino()
        self.assertEqual(self.core.tetrimino.coords[0],
                         self.core.tetrimino_ghost.coords[0])

    def test_do_progress(self):
        x, y = self.core.tetrimino.coords
        self.core.do_progress()
        self.assertEqual(self.core.tetrimino.coords, (x, y + 1))
