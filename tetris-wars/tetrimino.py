from grid import Grid


class Tetrimino:

    def __init__(self, coords, segments):
        self.__coords = coords
        self.__grid = Grid(coords=segments)

    def __iter__(self):
        return iter(self.__get_non_empty_cells())

    def __get_non_empty_cells(self):
        for y in range(self.__grid.size):
            for x in range(self.__grid.size):
                if self.__grid.cell((x, y)):
                    yield (self.coords[0] + x, self.coords[1] + y)

    @property
    def coords(self):
        return self.__coords

    @property
    def size(self):
        return self.__grid.size

    def cell(self, coords):
        x, y = coords
        x, y = (x - self.__coords[0], y - self.__coords[1])

        if min(x, y) < 0 or max(x, y) >= self.__grid.size:
            return False

        return self.__grid.cell((x, y))

    def rotate(self, dir):
        if(dir == 'left'):
            self.__grid.rotate_left()
        elif(dir == 'right'):
            self.__grid.rotate_right()
        else:
            raise KeyError('Invalid rotation direction "{}"'.format(dir))

    def move_down(self):
        x, y = self.__coords
        self.__coords = (x, y + 1)

    def move_left(self, times):
        x, y = self.__coords
        self.__coords = (x - times, y)


def create(type, coords):
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
