import copy
from enum import Enum
from .utils import *
from .grid import RotatableGrid


class Segment:

    def __init__(self, type):
        self._type = type

    @property
    def type(self):
        return self._type


class Tetrimino(RotatableGrid):
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
        L = 'L'
        J = 'J'
        T = 'T'
        I = 'I'
        S = 'S'
        Z = 'Z'
        O = 'O'

    def __init__(self,  type, x, y, segments):
        RotatableGrid.__init__(self, segments, Segment(type))
        self._type = type
        self._coords = (x, y)

    @property
    def view(self):
        return TetriminoView(self)

    @property
    def type(self):
        return self._type

    @property
    def coords(self):
        return self._coords

    @property
    def size(self):
        return self.measures[0]

    def _to_relative_coords(self, x, y):
        return tuple_sub((x, y), self._coords)

    def get_cell(self, x, y):
        x, y = self._to_relative_coords(x, y)
        if min(x, y) < 0 or max(x, y) >= self.size:
            return None
        return RotatableGrid.get_cell(self, x, y)

    def set_cell(self, x, y, value):
        x, y = self._to_relative_coords(x, y)
        if min(x, y) < 0 or max(x, y) >= self.size:
            return
        RotatableGrid.set_cell(self, x, y, value)

    def move_relative(self, x, y):
        self._coords = tuple_add((x, y), self._coords)

    def move_absolute(self, x, y):
        self._coords = (x, y)

    def __iter__(self):
        return iter(self._get_non_empty_cells())

    def _get_non_empty_cells(self):
        s = self.size
        for y in range(s):
            for x in range(s):
                segment = RotatableGrid.get_cell(self, x, y)
                if segment:
                    nx, ny = tuple_add(self.coords, (x, y))
                    yield (nx, ny, segment)


def create_tetrimino(type, x, y):
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
    return Tetrimino(type, x, y, tetriminos[type])


class TetriminoView():

    def __init__(self, tetrimino):
        self._tetrimino = tetrimino

    @property
    def size(self):
        return self._tetrimino.size

    @property
    def measures(self):
        return self._tetrimino.measures

    @property
    def type(self):
        return self._tetrimino.type

    @property
    def coords(self):
        return self._tetrimino.coords

    def get_cell(self, x, y):
        return self._tetrimino.get_cell(x, y)

    def __iter__(self):
        return iter(self._tetrimino._get_non_empty_cells())


class TetriminoUtils:

    @staticmethod
    def can_move(tetrimino, grid, x, y):
        new_tetrimino = copy.copy(tetrimino)
        new_tetrimino.move_relative(x, y)
        return not TetriminoUtils.is_placed_wrong(new_tetrimino, grid)

    @staticmethod
    def is_placed_wrong(tetrimino, grid):
        w, h = grid.measures
        for x, y, _ in tetrimino:
            if x < 0 or x >= w:
                return True
            if y < 0 or y >= h:
                return True
            if grid.get_cell(x, y):
                return True
        return False

    @staticmethod
    def hard_drop(tetrimino, grid):
        while TetriminoUtils.can_move(tetrimino, grid, 0, 1):
            tetrimino.move_relative(0, 1)

    @staticmethod
    def rotate(tetrimino, grid, dir):
        tetrimino.rotate(dir)

        while TetriminoUtils._is_left_of_grid(tetrimino, grid):
            tetrimino.move_relative(1, 0)

        while TetriminoUtils._is_right_of_grid(tetrimino, grid):
            tetrimino.move_relative(-1, 0)

        while TetriminoUtils.is_placed_wrong(tetrimino, grid):
            if tetrimino.coords[1] < 0:
                return
            tetrimino.move_relative(0, -1)

    @staticmethod
    def _is_right_of_grid(tetrimino, grid):
        w, h = grid.measures
        for x, y, _ in tetrimino:
            if x >= w:
                return True
        return False

    @staticmethod
    def _is_left_of_grid(tetrimino, grid):
        for x, y, _ in tetrimino:
            if x < 0:
                return True
        return False

    @staticmethod
    def calculate_actual_measures(tetrimino):
        maxx, maxy = 0, 0
        minx, miny = 4, 4
        for x, y, _ in tetrimino:
            maxx = max(maxx, x)
            maxy = max(maxy, y)
            minx = min(minx, x)
            miny = min(miny, y)
        return (minx, miny, maxx - minx + 1, maxy - miny + 1)

    @staticmethod
    def place_tetrimino(tetrimino, grid):
        for x, y, segment in tetrimino:
            grid.set_cell(x, y, segment)
