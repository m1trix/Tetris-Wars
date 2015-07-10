from enum import Enum


class GridView():

    def __init__(self, grid):
        self._grid = grid

    @property
    def measures(self):
        return self._grid.measures

    def get_cell(self, x, y):
        return self._grid.get_cell(x, y)


class Grid:

    def __init__(self, width, height):
        self._measures = width, height
        self._cells = self._create_cells(self._measures)

    def _create_cells(self, measures):
        w, h = measures
        cells = [None] * h
        for y in range(h):
            cells[y] = [None] * w
        return cells

    @property
    def measures(self):
        return self._measures

    @property
    def view(self):
        return GridView(self)

    def get_cell(self, x, y):
        return self._cells[y][x]

    def set_cell(self, x, y, value):
        self._cells[y][x] = value


ROTATION_OPERATORS = [
    lambda x, y, size: (x, y),
    lambda x, y, size: (y, size - 1 - x),
    lambda x, y, size: (size - 1 - x, size - 1 - y),
    lambda x, y, size: (size - 1 - y, x)
]
ROTATION_OPERATORS_COUNT = len(ROTATION_OPERATORS)


class Rotation(Enum):
    clockwise = 'cw'
    counterclockwise = 'ccw'


class RotationError(Exception):
    pass


class RotatableGrid(Grid):

    def __init__(self, cells, default_cell):
        size = self._calculate_size(cells)
        Grid.__init__(self, size, size)

        for x, y in cells:
            Grid.set_cell(self, x, y, default_cell)
        self._operator_index = 0

    def _calculate_size(self, cells):
        size = max(max(cells, key=lambda x: max(x))) + 1
        return size

    def get_cell(self, x, y):
        x, y = self._rotate_coords(x, y)
        return Grid.get_cell(self, x, y)

    def set_cell(self, x, y, value):
        x, y = self._rotate_coords(x, y)
        Grid.set_cell(self, x, y, value)

    def _rotate_coords(self, x, y):
        rotation_operator = ROTATION_OPERATORS[self._operator_index]
        return rotation_operator(x, y, self.measures[0])

    def rotate(self, dir):
        if dir == Rotation.clockwise:
            return self._rotate_grid(1)

        if dir == Rotation.counterclockwise:
            return self._rotate_grid(-1)

        raise RotationError("Unknown rotation direction {}".format(dir))

    def _rotate_grid(self, dir):
        self._operator_index += ROTATION_OPERATORS_COUNT + dir
        self._operator_index %= ROTATION_OPERATORS_COUNT


class GridUtils:

    @staticmethod
    def _is_line_full(grid, y):
        w, h = grid.measures
        for x in range(w):
            if not grid.get_cell(x, y):
                return False
        return True

    @staticmethod
    def get_full_lines(grid):
        w, h = grid.measures
        result = []
        for y in range(h):
            if GridUtils._is_line_full(grid, y):
                result.append(y)
        return result

    @staticmethod
    def clear_lines(grid, lines):
        w, h = grid.measures
        for y in lines:
            for x in range(w):
                grid.set_cell(x, y, None)

    @staticmethod
    def remove_lines(grid, lines):
        w, h = grid.measures
        counter = h - 1
        i = len(lines) - 1
        for y in range(grid.measures[1] - 1, -1, -1):
            if i >= 0 and lines.count(y) > 0:
                i -= 1
                continue
            for x in range(w):
                grid.set_cell(x, counter, grid.get_cell(x, y))
            counter -= 1
        for y in range(counter + 1):
            for x in range(w):
                grid.set_cell(x, y, None)
