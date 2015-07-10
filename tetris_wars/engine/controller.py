import time
from threading import Thread

from .renderer import RenderRequest
from .grid import *
from .action import Action
from .tetrimino import TetriminoUtils


class Controller:

    def __init__(self, game_core, timer, renderer_client):
        self._game_core = game_core
        self._easy_spin_core = game_core.easy_spin_core
        self._timer = timer
        self._renderer_client = renderer_client

    def _move_tetrimino(self, dirx, diry):
        if TetriminoUtils.can_move(
                self._game_core.falling_tetrimino,
                self._game_core.grid,
                dirx,
                diry):
            self._game_core.falling_tetrimino.move_relative(dirx, diry)
            self._game_core.refresh_ghost_tetrimino()

    def _rotate_tetrimino(self, dir):
        if self._easy_spin_core and self._easy_spin_core.is_running():
            if not self._easy_spin_core.add_cycle():
                return
        TetriminoUtils.rotate(
            self._game_core.falling_tetrimino,
            self._game_core.grid,
            dir)
        self._game_core.refresh_ghost_tetrimino()

    def _hard_drop(self):
        TetriminoUtils.hard_drop(
            self._game_core.falling_tetrimino,
            self._game_core.grid)
        self._timer.stop()
        self._easy_spin_core and self._easy_spin_core.hard_drop()

    def do_action(self, action):
        if not self._game_core.falling_tetrimino:
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
        self._renderer_client.request(RenderRequest.full)


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
