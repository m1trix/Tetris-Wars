from threading import Thread
from engine.action import Action
from engine.tetrimino import TetriminoUtils
from engine.grid import *
import time


class Controller:

    def __init__(self, game_core, timer):
        self._game_core = game_core
        self._timer = timer

    def _move_tetrimino(self, dirx, diry):
        if TetriminoUtils.can_move(
            self._game_core.tetrimino,
            self._game_core.grid,
            (dirx, diry)
        ):
            self._game_core.tetrimino.move_relative((dirx, diry))
            self._game_core.refresh_ghost_tetrimino()

    def _rotate_tetrimino(self, dir):
        TetriminoUtils.rotate(
            self._game_core.tetrimino,
            self._game_core.grid,
            dir)
        self._game_core.refresh_ghost_tetrimino()

    def _hard_drop(self):
        TetriminoUtils.hard_drop(
            self._game_core.tetrimino,
            self._game_core.grid)
        self._timer.reset()

    def do_action(self, action):
        if action == Action.move_left:
            self._move_tetrimino(-1, 0)
        elif action == Action.move_right:
            self._move_tetrimino(1, 0)
        elif action == Action.rotate_clockwise:
            self._rotate_tetrimino(Rotation.clockwise)
        elif action == Action.hard_drop:
            self._hard_drop()
        elif action == Action.soft_drop_on:
            self._timer.soft_drop_on()
        elif action == Action.soft_drop_off:
            self._timer.soft_drop_off()
        elif action == Action.hold:
            self._game_core.hold_tetrimino()


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
