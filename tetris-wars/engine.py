import grid
import tetrimino
import settings
import threading
import time

from random import randint


class Engine:

    def __init__(self, settings):
        self.__width = settings.grid_width
        self.__height = settings.grid_height
        size = max(self.__width, self.__height)
        self.__grid = grid.Grid(size=size)

        self.__soft_drop_time = settings.soft_drop_time
        self.__is_soft_drop_active = False

        self.__time = settings.game_speed
        self.__tetrimino = None
        self.__is_running = False

    def __spawn_tetrimino(self):
        types = ['L', 'J', 'S', 'Z', 'T', 'I', 'O']
        type = types[randint(0, len(types) - 1)]
        pos_x = self.__width // 2
        self.__tetrimino = tetrimino.create(type, (pos_x, 0))
        self.__tetrimino.move_left(self.__tetrimino.size // 2)

    def __progress_game(self):
        while self.is_running:
            if self.__is_soft_drop_active:
                time.sleep(self.__soft_drop_time)
            else:
                time.sleep(self.__time)
            self.__step()

    def __step(self):
        if self.__can_tetrimino_fall():
            self.__tetrimino.move_down()
            return

        for cell in self.__tetrimino:
            self.__grid.set(cell)
        self.__spawn_tetrimino()

    def __can_tetrimino_fall(self):
        """Tells if the tetrimino can fall one row
        down inside the current playing grid."""
        for cell in self.__tetrimino:
            x, y = cell
            if y + 1 == self.__height or self.__grid.cell((x, y + 1)):
                return False
        return True

    def execute(self):
        self.__is_running = True
        self.__spawn_tetrimino()
        progress = threading.Thread(target=self.__progress_game)
        progress.start()

    @property
    def is_running(self):
        return self.__is_running

    @property
    def tetrimino(self):
        return self.__tetrimino

    @property
    def grid(self):
        return self.__grid

    @property
    def measures(self):
        return (self.__width, self.__height)
