import engine.grid as grid
from engine.tetrimino import *
from engine.controller import Controller
import copy

import time

from random import randint


class Engine:

    class EngineController(Controller):

        def __init__(self, outer):
            self.__outer = outer

        def __move_tetrimino(self, dirx, diry):
            if self.__outer._can_move(self.__outer.tetrimino, (dirx, diry)):
                self.__outer.tetrimino.move_relative((dirx, diry))

        def do_action(self, action):
            if not self.__outer.is_running:
                return

            if action == Controller.Action.move_left:
                self.__move_tetrimino(-1, 0)
            elif action == Controller.Action.move_right:
                self.__move_tetrimino(1, 0)
            elif action == Controller.Action.rotate_clockwise:
                self.__outer.tetrimino.rotate(Rotation.clockwise)
            elif action == Controller.Action.hard_drop:
                self.__outer._hard_drop(self.__outer.tetrimino)
                self.__outer._is_interrupted = True
                return
            else:
                return

            self.__outer._move_ghost()

    def __init__(self, settings, renderer):
        self.__renderer = renderer
        self.__renderer.set_engine(self)

        self.__width = settings.grid_width
        self.__height = settings.grid_height
        self.__grid = grid.Grid(self.__width, self.__height)
        self.__soft_drop_time = settings.soft_drop_time
        self.__is_soft_drop_active = False

        self.__time = settings.game_speed
        self.__tetrimino = None
        self.__ghost = None
        self.__is_running = False

        self.__controller = self.EngineController(self)
        self._is_interrupted = False

    def __spawn_tetrimino(self):
        types = list(Tetrimino.Type)
        type = types[randint(0, len(types) - 1)]
        pos_x = self.__width // 2
        self.__tetrimino = Tetrimino.create(type, (pos_x, 0))
        self.__tetrimino.move_relative((-self.__tetrimino.size // 2, 0))

        self._move_ghost()

    def __wait(self, ms):
        while ms > 0:
            if self._is_interrupted:
                self._is_interrupted = False
                return
            time.sleep(0.001)
            ms -= 0.001

    def __progress_game(self):
        while self.is_running:
            self.__step()
            self.__renderer.render()
            if self.__is_soft_drop_active:
                self.__wait(self.__soft_drop_time)
            else:
                self.__wait(self.__time)

    def _move_ghost(self):
        self.__ghost = copy.copy(self.__tetrimino)
        self._hard_drop(self.__ghost)

    def _hard_drop(self, tetrimino):
        while self._can_move(tetrimino, (0, 1)):
            tetrimino.move_relative((0, 1))

    def __step(self):
        if self._can_move(self.__tetrimino, (0, 1)):
            return self.__tetrimino.move_relative((0, 1))

        for coords in self.__tetrimino:
            self.__grid.set_cell(coords, True)
        self.__spawn_tetrimino()

    def _can_move(self, tetrimino, dir):
        """Tells if the tetrimino can fall one row
        down inside the current playing grid."""
        dirx, diry = dir
        for cell in tetrimino:
            x, y = cell
            if x + dirx < 0 or x + dirx >= self.__width:
                return False
            if y + diry >= self.__height:
                return False
            if self.__grid.get_cell((x + dirx, y + diry)):
                return False
        return True

    def execute(self):
        self.__is_running = True
        self.__spawn_tetrimino()
        while self.__is_running:
            self.__progress_game()

    @property
    def is_running(self):
        return self.__is_running

    @property
    def tetrimino(self):
        return self.__tetrimino

    @property
    def ghost(self):
        return self.__ghost

    @property
    def grid(self):
        return self.__grid

    @property
    def controller(self):
        return self.__controller

    @property
    def measures(self):
        return (self.__width, self.__height)
