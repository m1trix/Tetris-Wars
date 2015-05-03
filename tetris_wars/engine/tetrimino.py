from engine.grid import *


class Tetrimino:
    """Tetrimino is thare main object of every Tetris game.

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

    def __init__(self, coords, segments):
        self.__coords = coords
        self.__grid = SpinGrid(segments)

    def __iter__(self):
        return iter(self.__get_non_empty_cells())

    def __get_non_empty_cells(self):
        w, h = self.__grid.measures
        for y in range(h):
            for x in range(w):
                if self.__grid.get_cell((x, y)):
                    yield (self.coords[0] + x, self.coords[1] + y)

    @property
    def coords(self):
        return self.__coords

    @property
    def size(self):
        return self.__grid.measures[0]

    def cell(self, coords):
        x, y = coords
        x, y = (x - self.__coords[0], y - self.__coords[1])

        if min(x, y) < 0 or max(x, y) >= self.__grid.measures[0]:
            return False

        return self.__grid.get_cell((x, y))

    def rotate(self, dir):
        self.__grid.rotate(dir)

    def move_to(self, coords):
        self.__coords = coords

    def move_down(self):
        x, y = self.__coords
        self.__coords = (x, y + 1)

    def move_left(self, times):
        x, y = self.__coords
        self.__coords = (x - times, y)


def create(type, coords):
    """ Factory for the 7 Tetriminos of the game. """
    tetriminos = {
        'L': [(0, 0), (0, 1), (0, 2), (1, 2)],
        'J': [(2, 0), (2, 1), (2, 2), (1, 2)],
        'T': [(0, 0), (1, 0), (2, 0), (1, 1)],
        'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
        'S': [(0, 1), (1, 1), (1, 0), (2, 0)],
        'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
        'O': [(0, 0), (0, 1), (1, 0), (1, 1)]
    }
    return Tetrimino(coords, tetriminos[type])
