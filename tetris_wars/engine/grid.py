from enum import Enum


class ImmutableGrid():

    def __init__(self, grid):
        self._grid = grid

    @property
    def measures(self):
        return self._grid.measures

    def get_cell(self, coords):
        return self._grid.get_cell(coords)


class Grid:

    def __init__(self, width, height):
        self._measures = width, height
        self._cells = self._create_cells(self._measures)

    def _create_cells(self, measures):
        cells = []
        w, h = measures
        for y in range(h):
            cells.append([None] * w)
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

    def immutable(self):
        return ImmutableGrid(self)


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

    def __init__(self, cells, default_cell):
        size = self._calculate_size(cells)
        super(SpinGrid, self).__init__(size, size)

        for coords in cells:
            Grid.set_cell(self, coords, default_cell)

        self._operator_index = 0

    def _calculate_size(self, cells):
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
        rotation_operator = ROTATION_OPERATORS[self._operator_index]
        return rotation_operator(coords, self._measures[0])

    def rotate(self, dir):
        if dir == Rotation.clockwise:
            return self._rotate_grid(1)

        if dir == Rotation.counterclockwise:
            return self._rotate_grid(-1)

        raise RotationError("Unknown rotation dir {}".format(dir))

    def _rotate_grid(self, dir):
        self._operator_index += ROTATION_OPERATORS_COUNT + dir
        self._operator_index %= ROTATION_OPERATORS_COUNT


class GridUtils:

    @staticmethod
    def get_full_lines(grid):
        w, h = grid.measures
        result = []
        for y in range(h):
            is_full = True
            for x in range(w):
                is_full = grid.get_cell((x, y)) and is_full
            if is_full:
                result.append(y)
        return result

    @staticmethod
    def clear_lines(grid, lines):
        w, h = grid.measures
        for y in lines:
            for x in range(w):
                grid.set_cell((x, y), None)

    @staticmethod
    def remove_lines(grid, lines):
        counter = grid.measures[1] - 1
        i = len(lines) - 1
        for y in range(grid.measures[1] - 1, -1, -1):
            if i >= 0 and y == lines[i]:
                i -= 1
                continue
            for x in range(grid.measures[0]):
                grid.set_cell((x, counter), grid.get_cell((x, y)))
            counter -= 1
