import time
import copy
from random import randint
from collections import deque

from .grid import Grid
from .grid import GridUtils
from .tetrimino import Tetrimino
from .tetrimino import TetriminoUtils
from .gravity import GravityCore
from .easy_spin import EasySpinCore
from .renderer import RenderRequest
from .generator import GeneratorCore


class GameCore:

    def __init__(self, settings, renderer_client):
        self._grid = Grid(
            settings['grid']['width'], settings['grid']['height'])
        self._renderer_client = renderer_client
        self._generator_core = GeneratorCore(settings)
        self._statistics_core = self._generator_core.statistics_core
        self._create_gravity_core(settings)
        self._create_easy_spin_core(settings)

        self._falling_tetrimino = None
        self._held_tetrimino = None
        self._ghost_tetrimino = None

        self._spawn_tetrimino()

    @property
    def view(self):
        return GameView(self)

    @property
    def generator_view(self):
        return self._generator_core.view

    @property
    def easy_spin_core(self):
        return self._easy_spin_core

    @property
    def grid(self):
        return self._grid

    @property
    def falling_tetrimino(self):
        return self._falling_tetrimino

    @property
    def ghost_tetrimino(self):
        return self._ghost_tetrimino

    @property
    def held_tetrimino(self):
        return self._held_tetrimino

    def _create_gravity_core(self, settings):
        self._gravity_core = None
        if settings['gravity']['use']:
            self._gravity_core = GravityCore(self._grid)
            self._gravity_speed = settings['gravity']['speed']

    def _create_easy_spin_core(self, settings):
        self._easy_spin_core = None
        if settings['easy_spin']['use']:
            self._easy_spin_core = EasySpinCore(settings)

    def _spawn_tetrimino(self):
        self._falling_tetrimino = self._generator_core.generate_tetrimino()
        self._reset_tetrimino_position()
        self.refresh_ghost_tetrimino()

        self._can_hold = True
        self._easy_spin_core and self._easy_spin_core.reset()
        return TetriminoUtils.can_move(
            self._falling_tetrimino, self.grid, 0, 1)

    def _reset_tetrimino_position(self):
        pos_x = self.grid.measures[0] // 2
        self._falling_tetrimino.move_absolute(pos_x, 0)
        self._falling_tetrimino.move_relative(
            -self._falling_tetrimino.size // 2, 0)

    def refresh_ghost_tetrimino(self):
        self._ghost_tetrimino = copy.copy(self._falling_tetrimino)
        TetriminoUtils.hard_drop(self._ghost_tetrimino, self.grid)

    def _clear_lines(self):
        lines = GridUtils.get_full_lines(self.grid)
        self._statistics_core.note_lines_clear(len(lines))
        if not lines:
            return False
        w, h = self.grid.measures
        self._renderer_client.request(RenderRequest.line_clear, lines).wait()
        if self._gravity_core:
            GridUtils.clear_lines(self.grid, lines)
            self._gravity_core.regenerate_grid()
        GridUtils.remove_lines(self.grid, lines)
        return True

    def hold_tetrimino(self):
        if not self._can_hold:
            self._renderer_client.request(RenderRequest.cannot_hold)
            return
        held = self._held_tetrimino
        self._held_tetrimino = self._falling_tetrimino
        self._falling_tetrimino = held
        self._held_tetrimino.move_absolute(0, 0)

        if self._falling_tetrimino:
            self._reset_tetrimino_position()
            self.refresh_ghost_tetrimino()
            self._easy_spin_core and self._easy_spin_core.hard_reset()
        else:
            self._spawn_tetrimino()
        self._can_hold = False

    def do_progress(self):
        if TetriminoUtils.can_move(self._falling_tetrimino, self.grid, 0, 1):
            self._falling_tetrimino.move_relative(0, 1)
            self._trigger_render()
            if not self._easy_spin_core:
                return True
            if TetriminoUtils.can_move(
                    self._falling_tetrimino, self.grid, 0, 1):
                return True
        if self._wait_easy_spin():
            return True

        TetriminoUtils.place_tetrimino(self._falling_tetrimino, self._grid)
        self._falling_tetrimino = None
        self._ghost_tetrimino = None

        self._clear_lines() and self._trigger_gravity()
        self._trigger_render()

        game_over = not self._spawn_tetrimino()
        if game_over:
            self._renderer_client.request(RenderRequest.game_over).wait()
        return not game_over

    def _wait_easy_spin(self):
        if not self._easy_spin_core:
            return False
        if self._easy_spin_core.is_running():
            return True
        return self._easy_spin_core.start()

    def _trigger_gravity(self):
        if not self._gravity_core:
            return
        time.sleep(self._gravity_speed)
        gravity_runs = True
        while gravity_runs:
            gravity_runs = False
            while self._gravity_core.do_progress():
                self._trigger_render()
                time.sleep(self._gravity_speed)
                gravity_runs = True
            if self._clear_lines():
                time.sleep(self._gravity_speed)

    def _trigger_render(self):
        self._renderer_client.request(RenderRequest.full)


class GameView:

    def __init__(self, game_core):
        self._grid_view = game_core.grid.view
        self._generator_view = game_core.generator_view
        self._game_core = game_core

    @property
    def generator_view(self):
        return self._generator_view

    @property
    def grid(self):
        return self._grid_view

    @property
    def falling_tetrimino(self):
        return (self._game_core.falling_tetrimino
                and self._game_core.falling_tetrimino.view)

    @property
    def ghost_tetrimino(self):
        return (self._game_core.ghost_tetrimino
                and self._game_core.ghost_tetrimino.view)

    @property
    def held_tetrimino(self):
        return (self._game_core.held_tetrimino
                and self._game_core.held_tetrimino.view)
