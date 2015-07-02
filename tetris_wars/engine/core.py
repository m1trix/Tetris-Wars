from engine.tetrimino import *
from engine.grid import GridUtils
from random import randint


class GameCore:

    def __init__(self, settings):
        self.grid = Grid(settings.grid_width, settings.grid_height)
        self.tetrimino = None
        self.tetrimino_hold = None
        self.tetrimino_ghost = None
        self._can_hold = False
        self._spawn_tetrimino()

    def _reset_tetrimino_position(self):
        pos_x = self.grid.measures[0] // 2
        self.tetrimino.move_absolute((pos_x, 0))
        self.tetrimino.move_relative((-self.tetrimino.size // 2, 0))

    def _spawn_tetrimino(self):
        types = list(Tetrimino.Type)
        type = types[randint(0, len(types) - 1)]

        self.tetrimino = Tetrimino.create(type, (0, 0))
        self._reset_tetrimino_position()

        self.refresh_ghost_tetrimino()
        self._can_hold = True

    def refresh_ghost_tetrimino(self):
        self.tetrimino_ghost = copy.copy(self.tetrimino)
        TetriminoUtils.hard_drop(self.tetrimino_ghost, self.grid)

    def _clear_lines(self):
        lines = GridUtils.get_full_lines(self.grid)
        if lines:
            GridUtils.clear_full_lines(self.grid, lines)

    def hold_tetrimino(self):
        if not self._can_hold:
            return
        hold = self.tetrimino_hold
        self.tetrimino_hold = self.tetrimino
        self.tetrimino = hold
        self.tetrimino_hold.move_absolute((0, 0))

        if self.tetrimino:
            self._reset_tetrimino_position()
            self.refresh_ghost_tetrimino()
        else:
            self._spawn_tetrimino()
        self._can_hold = False

    def do_progress(self):
        if TetriminoUtils.can_move(self.tetrimino, self.grid, (0, 1)):
            return self.tetrimino.move_relative((0, 1))
        for (coords, value) in self.tetrimino:
            self.grid.set_cell(coords, value)
        self._clear_lines()
        self._spawn_tetrimino()
