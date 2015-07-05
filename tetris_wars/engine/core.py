from engine.tetrimino import *
from engine.grid import GridUtils
from random import randint
from collections import deque
from engine.gravity import GravityEngine
from engine.renderer import RendererCore
from engine.renderer import RenderRequest
from engine.easy_spin import EasySpinEngine
import time


class GameCore:

    def __init__(self, settings):
        self.grid = Grid(settings.grid_width, settings.grid_height)
        self.tetrimino = None
        self.tetrimino_hold = None
        self.tetrimino_ghost = None
        self.queue = deque([])
        self.renderer_core = RendererCore(settings, self)

        self._use_easy_spin = settings.use_easy_spin
        self.easy_spin = None
        if self._use_easy_spin:
            self.easy_spin = EasySpinEngine(settings)

        self._fill_queue(settings.queue_size)

        self._game_speed = settings.game_speed
        self._gravity_speed = settings.gravity_speed
        self._use_gravity = settings.use_gravity
        if self._use_gravity:
            self._gravity = GravityEngine(self.grid)

        self._can_hold = False
        self._spawn_tetrimino()

    def _fill_queue(self, count):
        for i in range(count):
            self.queue.append(self._create_random_tetrimino())

    def _reset_tetrimino_position(self):
        pos_x = self.grid.measures[0] // 2
        self.tetrimino.move_absolute((pos_x, 0))
        self.tetrimino.move_relative((-self.tetrimino.size // 2, 0))

    def _create_random_tetrimino(self):
        types = list(Tetrimino.Type)
        type = types[randint(0, len(types) - 1)]
        return Tetrimino.create(type, (0, 0))

    def _spawn_tetrimino(self):
        self.tetrimino = self.queue.popleft()
        self.queue.append(self._create_random_tetrimino())
        self._reset_tetrimino_position()

        self.refresh_ghost_tetrimino()
        self._can_hold = True
        return TetriminoUtils.can_move(self.tetrimino, self.grid, (0, 1))

    def refresh_ghost_tetrimino(self):
        self.tetrimino_ghost = copy.copy(self.tetrimino)
        TetriminoUtils.hard_drop(self.tetrimino_ghost, self.grid)

    def _clear_lines(self):
        lines = GridUtils.get_full_lines(self.grid)
        if not lines:
            return False
        w, h = self.grid.measures
        self.renderer_core.make_render_request(
            (RenderRequest.line_clear, (w, h, lines)))
        if self._use_gravity:
            GridUtils.clear_lines(self.grid, lines)
            self._gravity.regenerate_grid()
        GridUtils.remove_lines(self.grid, lines)
        return True

    def hold_tetrimino(self):
        if not self._can_hold:
            return
        hold = self.tetrimino_hold
        self.tetrimino_hold = self.tetrimino
        self.tetrimino = hold
        self.tetrimino_hold.move_absolute((0, 0))

        if self.tetrimino:
            self._reset_tetrimino_position()
            self.refresh_ghost_tetrimino()
        else:
            self._spawn_tetrimino()
        self._can_hold = False

    def do_progress(self):
        if TetriminoUtils.can_move(self.tetrimino, self.grid, (0, 1)):
            self.tetrimino.move_relative((0, 1))
            self.render()
            return True

        if self._use_easy_spin:
            self.easy_spin.reset()
            self.easy_spin.start_countdown()

        for coords, value in self.tetrimino:
            self.grid.set_cell(coords, value)
        self.tetrimino = None
        self.tetrimino_ghost = None

        if self._clear_lines() and self._use_gravity:
            self.render()
            time.sleep(self._gravity_speed)
            self._progress_gravity()

        self.render()
        return self._spawn_tetrimino()

    def _progress_gravity(self):
        change = True
        while change:
            change = False
            while self._gravity.do_progress():
                self.render()
                time.sleep(self._gravity_speed)
                change = True
            if self._clear_lines():
                time.sleep(self._gravity_speed)

    def render(self):
        self.renderer_core.make_render_request(
            (RenderRequest.full,
                (copy.copy(self.grid),
                    copy.copy(self.tetrimino),
                    copy.copy(self.tetrimino_ghost),
                    copy.copy(self.tetrimino_hold),
                    copy.copy(self.queue))))
