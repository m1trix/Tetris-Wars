from engine.utils import *
from engine.grid import *
from enum import Enum


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
        self.__coords = coords

    @property
    def coords(self):
        return self.__coords

    @property
    def size(self):
        return self.measures[0]

    def _to_relative_coords(self, coords):
        return tuple_sub(coords, self.__coords)

    def get_cell(self, coords):
        coords = self._to_relative_coords(coords)
        if min(coords) < 0 or max(coords) >= self.size:
            return False
        return super(Tetrimino, self).get_cell(coords)

    def set_cell(self, coords, value):
        coords = self._to_relative_coords(coords)
        super(Tetrimino, self).set_cell(coords, value)

    def move_relative(self, coords):
        self.__coords = tuple_add(coords, self.__coords)

    def move_absolute(self, coords):
        self.__coords = coords

    def __iter__(self):
        return iter(self.__get_non_empty_cells())

    def __get_non_empty_cells(self):
        w, h = self.measures
        for y in range(h):
            for x in range(w):
                coords = tuple_add(self.coords, (x, y))
                if self.get_cell(coords):
                    yield coords
