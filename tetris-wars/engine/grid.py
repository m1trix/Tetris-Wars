from functools import reduce


ROTATION_OPERATORS_COUNT = 4

rotation_operators = [
    lambda coords, size: coords,
    lambda coords, size: (coords[1], size - 1 - coords[0]),
    lambda coords, size: (size - 1 - coords[0], size - 1 - coords[1]),
    lambda coords, size: (size - 1 - coords[1], coords[0])
]


class Grid:

    def __init__(self, coords=[], size=-1):
        self.__size = size
        if self.__size == -1:
            self.__size = self.__calculate_size(coords)

        self.__grid = self.__create_grid(self.__size)
        self.__rotation = 0

        for x, y in coords:
            self.__grid[y][x] = True

    @property
    def size(self):
        return self.__size

    def __calculate_size(self, coords):
        return reduce(lambda m, x: max(x[0], x[1], m), coords, 0) + 1

    def __create_grid(self, size):
        grid = []

        for i in range(size):
            grid.append([])
            for _ in range(size):
                grid[i].append(False)

        return grid

    def cell(self, coords):
        x, y = rotation_operators[self.__rotation](coords, self.size)
        return self.__grid[y][x]

    def set(self, coords):
        x, y = coords
        self.__grid[y][x] = True

    def rotate_clockwise(self):
        self.__rotation = (self.__rotation + 1) % ROTATION_OPERATORS_COUNT

    def rotate_counter_clockwise(self):
        self.__rotation += ROTATION_OPERATORS_COUNT - 1
        self.__rotation %= ROTATION_OPERATORS_COUNT
