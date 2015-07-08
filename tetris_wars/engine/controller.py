from threading import Thread
from .grid import *
from .action import Action
from .tetrimino import TetriminoUtils
import time


class Controller:

    def __init__(self, core_units):
        self._game_core = core_units[0]
        self._easy_spin_core = core_units[1]
        self._timer = core_units[2]

    def _move_tetrimino(self, dirx, diry):
        if TetriminoUtils.can_move(
                self._game_core.tetrimino, self._game_core.grid, dirx, diry):
            self._game_core.tetrimino.move_relative(dirx, diry)
            self._game_core.refresh_ghost_tetrimino()

    def _rotate_tetrimino(self, dir):
        if self._easy_spin_core and self._easy_spin_core.is_running():
            if not self._easy_spin_core.add_cycle():
                return
        TetriminoUtils.rotate(
            self._game_core.tetrimino,
            self._game_core.grid,
            dir)
        self._game_core.refresh_ghost_tetrimino()

    def _hard_drop(self):
        TetriminoUtils.hard_drop(
            self._game_core.tetrimino,
            self._game_core.grid)
        self._timer.stop()
        self._easy_spin_core and self._easy_spin_core.hard_drop()

    def do_action(self, action):
        if not self._game_core.tetrimino:
            return
        if action == Action.move_left:
            self._move_tetrimino(-1, 0)
        elif action == Action.move_right:
            self._move_tetrimino(1, 0)
        elif action == Action.rotate_clockwise:
            self._rotate_tetrimino(Rotation.clockwise)
        elif action == Action.hard_drop:
            self._hard_drop()
            return
        elif action == Action.soft_drop_on:
            self._timer.soft_drop_on()
        elif action == Action.soft_drop_off:
            self._timer.soft_drop_off()
        elif action == Action.hold:
            self._game_core.hold_tetrimino()
        self._game_core.trigger_render()


class ActionListener:

    def __init__(self, controller):
        self._controller = controller
        self._is_running = False

    def _detect_actions(self):
        pass

    def _loop(self):
        self._is_running = True
        while self._is_running:
            for action in self._detect_actions():
                self._controller.do_action(action)
            time.sleep(0.075)

    def start(self):
        Thread(target=self._loop).start()

    def stop(self):
        self._is_running = False
