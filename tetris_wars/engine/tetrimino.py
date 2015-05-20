from engine.utils import *
from engine.grid import *
from enum import Enum
import copy


class Tetrimino(SpinGrid):
    """
    The tetrimino is the main object of every Tetris game.

    Tetriminos are the 4-piece figures that one must pile
    in order to achieve victory. There are 7 unique tetriminos.
    L, J, Z, S, T, I and O tetriminos.

    Each Tetrimino has coordinates - a pair of integers. They
    represent the global position of the Tetrimino inside the
    playing grid.

    Each Tetrimino has a square grid of booleans. They have
    relative coordinates, starting at (0, 0). The grid holds
    the segments of the Tetrimino and it is large enough for
    them to be able to rotate inside it.
    """

    class Type(Enum):
        L = 'l'
        J = 'j'
        T = 't'
        I = 'i'
        S = 's'
        Z = 'z'
        O = 'o'

    @staticmethod
    def create(type, coords):
        """ Factory method for the 7 Tetriminos of the game. """
        tetriminos = {
            Tetrimino.Type.L: [(0, 0), (0, 1), (0, 2), (1, 2)],
            Tetrimino.Type.J: [(2, 0), (2, 1), (2, 2), (1, 2)],
            Tetrimino.Type.T: [(0, 0), (1, 0), (2, 0), (1, 1)],
            Tetrimino.Type.I: [(0, 1), (1, 1), (2, 1), (3, 1)],
            Tetrimino.Type.S: [(0, 1), (1, 1), (1, 0), (2, 0)],
            Tetrimino.Type.Z: [(0, 0), (1, 0), (1, 1), (2, 1)],
            Tetrimino.Type.O: [(0, 0), (0, 1), (1, 0), (1, 1)]
        }
        return Tetrimino(coords, tetriminos[type])

    def __init__(self, coords, segments):
        super(Tetrimino, self).__init__(segments)
        self._coords = coords

    @property
    def coords(self):
        return self._coords

    @property
    def size(self):
        return self.measures[0]

    def _to_relative_coords(self, coords):
        return tuple_sub(coords, self._coords)

    def get_cell(self, coords):
        coords = self._to_relative_coords(coords)
        if min(coords) < 0 or max(coords) >= self.size:
            return False
        return super(Tetrimino, self).get_cell(coords)

    def set_cell(self, coords, value):
        coords = self._to_relative_coords(coords)
        super(Tetrimino, self).set_cell(coords, value)

    def move_relative(self, coords):
        self._coords = tuple_add(coords, self._coords)

    def move_absolute(self, coords):
        self._coords = coords

    def __iter__(self):
        return iter(self._get_non_empty_cells())

    def _get_non_empty_cells(self):
        w, h = self.measures
        for y in range(h):
            for x in range(w):
                coords = tuple_add(self.coords, (x, y))
                if self.get_cell(coords):
                    yield coords


class TetriminoUtils:

    @staticmethod
    def can_move(tetrimino, grid, dir):
        new_tetrimino = copy.copy(tetrimino)
        new_tetrimino.move_relative(dir)
        return not TetriminoUtils.is_placed_wrong(new_tetrimino, grid)

    @staticmethod
    def is_placed_wrong(tetrimino, grid):
        width, height = grid.measures
        for x, y in tetrimino:
            if x < 0 or x >= width:
                return True
            if y < 0 or y >= height:
                return True
            if grid.get_cell((x, y)):
                return True
        return False

    @staticmethod
    def hard_drop(tetrimino, grid):
        while TetriminoUtils.can_move(tetrimino, grid, (0, 1)):
            tetrimino.move_relative((0, 1))

    @staticmethod
    def rotate(tetrimino, grid, dir):
        tetrimino.rotate(dir)

        while TetriminoUtils._is_left_of_grid(tetrimino, grid):
            tetrimino.move_relative((1, 0))

        while TetriminoUtils._is_right_of_grid(tetrimino, grid):
            tetrimino.move_relative((-1, 0))

        while TetriminoUtils.is_placed_wrong(tetrimino, grid):
            tetrimino.move_relative((0, -1))

    @staticmethod
    def _is_right_of_grid(tetrimino, grid):
        for x, y in tetrimino:
            if x >= grid.measures[0]:
                return True
        return False

    @staticmethod
    def _is_left_of_grid(tetrimino, grid):
        for x, y in tetrimino:
            if x < 0:
                return True
        return False
