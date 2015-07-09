import unittest
from ..engine.statistics import *
from ..engine.tetrimino import *


class TestStatisticsCore(unittest.TestCase):

    def setUp(self):
        self.statistics = StatisticsCore()

    def test_note_tetrimino_spawn(self):
        tetrimino = create_tetrimino(Tetrimino.Type.L, 0, 0)
        self.statistics.note_tetrimino_spawn(tetrimino)
        self.assertIn((Tetrimino.Type.L, 1), self.statistics.statistics)
        self.assertIn((Tetrimino.Type.L, 1), self.statistics.view.statistics)

        tetrimino = create_tetrimino(Tetrimino.Type.L, 0, 0)
        self.statistics.note_tetrimino_spawn(tetrimino)
        self.assertIn((Tetrimino.Type.L, 2), self.statistics.statistics)
        self.assertIn((Tetrimino.Type.L, 2), self.statistics.view.statistics)

        tetrimino = create_tetrimino(Tetrimino.Type.Z, 0, 0)
        self.statistics.note_tetrimino_spawn(tetrimino)
        self.assertIn((Tetrimino.Type.Z, 1), self.statistics.statistics)
        self.assertIn((Tetrimino.Type.Z, 1), self.statistics.view.statistics)

    def test_note_lines_clear(self):
        self.statistics.note_lines_clear(1)
        self.assertEqual(self.statistics.score, 100)
        self.assertEqual(self.statistics.view.score, 100)

        self.statistics.note_lines_clear(4)
        self.assertEqual(self.statistics.score, 900)
        self.assertEqual(self.statistics.view.score, 900)

        self.statistics.note_lines_clear(3)
        self.assertEqual(self.statistics.score, 1200)
        self.assertEqual(self.statistics.view.score, 1200)

        self.statistics.note_lines_clear(4)
        self.assertEqual(self.statistics.score, 2000)
        self.assertEqual(self.statistics.view.score, 2000)

        self.statistics.note_lines_clear(4)
        self.assertEqual(self.statistics.score, 3200)
        self.assertEqual(self.statistics.view.score, 3200)
