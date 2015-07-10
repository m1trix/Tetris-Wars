from unittest import TestCase
from ..engine.gravity import *
from ..engine.tetrimino import *
from ..engine.grid import *


class TestGravityCore(TestCase):

    def setUp(self):
        self.grid = Grid(6, 8)
        self.gravity = GravityCore(self.grid)

    def test_gravity(self):
        tetrimino = create_tetrimino(Tetrimino.Type.L, 0, 5)
        TetriminoUtils.place_tetrimino(tetrimino, self.grid)

        tetrimino = create_tetrimino(Tetrimino.Type.T, 0, 5)
        tetrimino.rotate(Rotation.clockwise)
        TetriminoUtils.place_tetrimino(tetrimino, self.grid)

        tetrimino = create_tetrimino(Tetrimino.Type.S, -1, 3)
        tetrimino.rotate(Rotation.clockwise)
        TetriminoUtils.place_tetrimino(tetrimino, self.grid)

        tetrimino = create_tetrimino(Tetrimino.Type.Z, 4, 5)
        tetrimino.rotate(Rotation.counterclockwise)
        TetriminoUtils.place_tetrimino(tetrimino, self.grid)

        tetrimino = create_tetrimino(Tetrimino.Type.I, 4, 1)
        tetrimino.rotate(Rotation.counterclockwise)
        TetriminoUtils.place_tetrimino(tetrimino, self.grid)

        tetrimino = create_tetrimino(Tetrimino.Type.L, 3, 1)
        TetriminoUtils.place_tetrimino(tetrimino, self.grid)
        # Simulation:
        # ......[]..()
        # ......[]..()
        # []....[][]()
        # [][]......()
        # ()[]{}....{}
        # (){}{}..{}{}
        # ()(){}..{}..

        while self.gravity.do_progress():
            continue
        lines = GridUtils.get_full_lines(self.grid)
        self.assertEqual(lines, [5])

        GridUtils.clear_lines(self.grid, lines)
        self.gravity.regenerate_grid()
        GridUtils.remove_lines(self.grid, lines)
        # Expectations:
        # ..........()    # ..........()    # ..........()
        # ..........()    # ..........()    # ..........()
        # []....[]..()    # []....[]..()    # []....[]..()
        # [][]..[]..()    # [][]..[]..()    # [][]..[]..()
        # ()[]{}[][]{}    # ============    # ............
        # (){}{}..{}{}    # (){}{}..[][]    # (){}{}..[][]
        # ()(){}..{}..    # ()(){}..[]..    # ()(){}..[]..

        while self.gravity.do_progress():
            continue
        lines = GridUtils.get_full_lines(self.grid)
        self.assertEqual(lines, [6])

        GridUtils.clear_lines(self.grid, lines)
        self.gravity.regenerate_grid()
        GridUtils.remove_lines(self.grid, lines)
        # Expectations:
        # ............    # ............    # ............
        # ..........()    # ..........()    # ..........()
        # ..........()    # ..........()    # ..........()
        # []........()    # []........()    # []....[]..()
        # [][]......()    # [][]......()    # [][]..[]..()
        # (){}{}[]{}{}    # ============    # ............
        # ()(){}[]{}..    # ()(){}[][]..    # ()(){}..[]..

        while self.gravity.do_progress():
            continue
        lines = GridUtils.get_full_lines(self.grid)
        self.assertEqual(lines, [7])
        # Expectations:
        # ............    # ............    # ............
        # ............    # ............    # ............
        # ............    # ............    # ..........()
        # ..........()    # ..........()    # ..........()
        # []........()    # []........()    # []....[]..()
        # [][]......()    # [][]......()    # [][]..[]..()
        # ()(){}[]{}()    # ============    # ............
