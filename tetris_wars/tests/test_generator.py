from unittest import TestCase
from collections import deque
from ..engine.generator import *


class GeneratorCoreMock(GeneratorCore):

    def __init__(self, tetriminos, settings):
        self.tetriminos = deque(tetriminos)
        GeneratorCore.__init__(self, settings)

    def _create_random_tetrimino(self):
        return self.tetriminos.popleft()


class TestGeneratorCore(TestCase):

    def test_generate_tetrimino(self):
        tetriminos = [
            create_tetrimino(Tetrimino.Type.L, 0, 0),
            create_tetrimino(Tetrimino.Type.L, 0, 0),
            create_tetrimino(Tetrimino.Type.L, 0, 0),
            create_tetrimino(Tetrimino.Type.Z, 0, 0)]
        generator = GeneratorCoreMock(tetriminos, {
            'generator': {
                'queue_size': 2,
                'repetition_limit': 2
            }
        })
        self.assertIn(tetriminos[0], generator.queue)
        self.assertIn(tetriminos[1], generator.queue)

        self.assertEqual(tetriminos[0], generator.generate_tetrimino())
        self.assertNotIn(tetriminos[2], generator.queue)
        self.assertIn(tetriminos[3], generator.queue)

        # Tetriminos enter the statistics after they are popped from the queue
        statistics_core = generator.statistics_core
        self.assertIn((Tetrimino.Type.L, 1), statistics_core.statistics)
        self.assertIn((Tetrimino.Type.Z, 0), statistics_core.statistics)

    def test_generator_with_no_queue(self):
        tetriminos = [
            create_tetrimino(Tetrimino.Type.L, 0, 0),
            create_tetrimino(Tetrimino.Type.L, 0, 0),
            create_tetrimino(Tetrimino.Type.L, 0, 0),
            create_tetrimino(Tetrimino.Type.Z, 0, 0)]
        generator = GeneratorCoreMock(tetriminos, {
            'generator': {
                'queue_size': 0,
                'repetition_limit': 2
            }
        })

        self.assertEqual(generator.view.queue, [])
        self.assertEqual(tetriminos[0], generator.generate_tetrimino())
        self.assertEqual(tetriminos[1], generator.generate_tetrimino())
        self.assertEqual(tetriminos[3], generator.generate_tetrimino())

        statistics_view = generator.view.statistics_view
        self.assertIn((Tetrimino.Type.L, 2), statistics_view.statistics)
        self.assertIn((Tetrimino.Type.Z, 1), statistics_view.statistics)
