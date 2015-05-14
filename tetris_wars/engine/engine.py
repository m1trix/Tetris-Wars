import engine.grid as grid
from engine.tetrimino import *
from engine.controller import Controller
import copy

import time

from random import randint


#TODO PEP-8
class Engine:

    class EngineController(Controller):

        def __init__(self, outer):
            self.__outer = outer

        def __move_tetrimino(self, dirx, diry):
            if TetriminoUtils.can_move(self.__outer.tetrimino, self.__outer.grid, (dirx, diry)):
                self.__outer.tetrimino.move_relative((dirx, diry))

        def do_action(self, action):
            if not self.__outer.is_running:
                return

            if action == Controller.Action.move_left:
                self.__move_tetrimino(-1, 0)
            elif action == Controller.Action.move_right:
                self.__move_tetrimino(1, 0)
            elif action == Controller.Action.rotate_clockwise:
                TetriminoUtils.rotate(self.__outer.tetrimino, self.__outer.grid, Rotation.clockwise)
            elif action == Controller.Action.hard_drop:
                TetriminoUtils.hard_drop(self.__outer.tetrimino, self.__outer.grid)
                self.__outer._is_interrupted = True
                self.__outer._is_changed = False
                return
            elif action == Controller.Action.soft_drop_on:
                self.__outer.set_soft_drop(True)
            elif action == Controller.Action.soft_drop_off:
                self.__outer.set_soft_drop(False)
            else:
                return

            self.__outer._is_changed = True
            self.__outer._move_ghost()
            self.__outer._renderer.render()

    def __init__(self, settings, renderer):
        self._renderer = renderer
        self._renderer.set_engine(self)

        self.__width = settings.grid_width
        self.__height = settings.grid_height
        self.__grid = grid.Grid(self.__width, self.__height)
        self.__soft_drop_time = settings.soft_drop_time
        self.__is_soft_drop_active = False

        self.__tetrimino = None
        self.__ghost = None
        self.__is_running = False

        self.__controller = self.EngineController(self)
        self._is_interrupted = False
        self._is_changed = False

        self._game_timer = 0.0
        self._game_step_rate = settings.game_speed

        self._render_timer = 0.0
        self._game_render_rate = 1 / settings.fps

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

    def set_soft_drop(self, b):
        self.__is_soft_drop_active = b

    def __progress_game(self):
        beg = time.time()
        if self._game_timer <= 0:
            self.__step()
            self._game_timer = self._game_step_rate
        if self._render_timer <= 0:
            self._renderer.render()
            self._render_timer = self._game_render_rate
        pause = min(self._game_timer, self._render_timer)
        self._game_timer -= pause
        self._render_timer -= pause
        end = time.time()
        time.sleep(max(0, pause - end + beg))

    def _move_ghost(self):
        self.__ghost = copy.copy(self.__tetrimino)
        TetriminoUtils.hard_drop(self.__ghost, self.__grid)

    def __step(self):
        if TetriminoUtils.can_move(self.__tetrimino, self.__grid, (0, 1)):
            return self.__tetrimino.move_relative((0, 1))
        for coords in self.__tetrimino:
            self.__grid.set_cell(coords, True)
        self.__spawn_tetrimino()

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
