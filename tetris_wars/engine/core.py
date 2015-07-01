from engine.tetrimino import *
from random import randint


class GameCore:

    def __init__(self, settings):
        self.grid = Grid(settings.grid_width, settings.grid_height)
        self.tetrimino = None
        self.tetrimino_ghost = None
        self._spawn_tetrimino()

    def _spawn_tetrimino(self):
        types = list(Tetrimino.Type)
        type = types[randint(0, len(types) - 1)]
        pos_x = self.grid.measures[0] // 2

        self.tetrimino = Tetrimino.create(type, (pos_x, 0))
        self.tetrimino.move_relative((-self.tetrimino.size // 2, 0))

        self.refresh_ghost_tetrimino()

    def refresh_ghost_tetrimino(self):
        self.tetrimino_ghost = copy.copy(self.tetrimino)
        TetriminoUtils.hard_drop(self.tetrimino_ghost, self.grid)

    def do_progress(self):
        if TetriminoUtils.can_move(self.tetrimino, self.grid, (0, 1)):
            return self.tetrimino.move_relative((0, 1))
        for (coords, value) in self.tetrimino:
            self.grid.set_cell(coords, value)
        self._spawn_tetrimino()
