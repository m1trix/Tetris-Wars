from enum import Enum


class Grid:

    def __init__(self, width, height):
        self._measures = width, height
        self._cells = self._create_cells(self._measures)

    def _create_cells(self, measures):
        cells = []
        w, h = measures
        for y in range(h):
            cells.append([False] * w)
        return cells

    def get_cell(self, coords):
        x, y = coords
        return self._cells[y][x]

    def set_cell(self, coords, value):
        x, y = coords
        self._cells[y][x] = value

    @property
    def measures(self):
        return self._measures


ROTATION_OPERATORS = [
    lambda coords, size: coords,
    lambda coords, size: (coords[1], size - 1 - coords[0]),
    lambda coords, size: (size - 1 - coords[0], size - 1 - coords[1]),
    lambda coords, size: (size - 1 - coords[1], coords[0])
]
ROTATION_OPERATORS_COUNT = len(ROTATION_OPERATORS)


class Rotation(Enum):
    clockwise = 'cw'
    counterclockwise = 'ccw'


class RotationError(Exception):
    pass


class SpinGrid(Grid):

    def __init__(self, cells):
        size = self.__calculate_size(cells)
        super(SpinGrid, self).__init__(size, size)

        for coords in cells:
            Grid.set_cell(self, coords, True)

        self.__operator_index = 0

    def __calculate_size(self, cells):
        w, h = 0, 0
        for x, y in cells:
            w, h = max(w, x), max(h, y)
        return max(0, w + 1, h + 1)

    def get_cell(self, coords):
        coords = self._rotate_coords(coords)
        return Grid.get_cell(self, coords)

    def set_cell(self, coords, value):
        coords = self._rotate_coords(coords)
        Grid.set_cell(self, coords, value)

    def _rotate_coords(self, coords):
        rotation_operator = ROTATION_OPERATORS[self.__operator_index]
        return rotation_operator(coords, self._measures[0])

    def rotate(self, dir):
        if dir == Rotation.clockwise:
            return self.__rotate_grid(1)

        if dir == Rotation.counterclockwise:
            return self.__rotate_grid(-1)

        raise RotationError("Unknown rotation dir {}".format(dir))

    def __rotate_grid(self, dir):
        self.__operator_index += ROTATION_OPERATORS_COUNT + dir
        self.__operator_index %= ROTATION_OPERATORS_COUNT
