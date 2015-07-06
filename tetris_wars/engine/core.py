from engine.tetrimino import *
from engine.grid import GridUtils
from random import randint
from collections import deque
from engine.gravity import GravityCore
from engine.renderer import RendererCore
from engine.renderer import RenderRequest
from engine.easy_spin import EasySpinCore
import time


class GameCore:

    def __init__(self, settings, grid, easy_spin_core, gravity_core):
        self.grid = grid
        self._gravity_core = gravity_core
        self._easy_spin_core = easy_spin_core
        self.renderer_core = RendererCore(settings, self)

        self.tetrimino = None
        self.tetrimino_hold = None
        self.tetrimino_ghost = None

        self.queue = deque([])
        self._fill_queue(settings.queue_size)

        self._gravity_speed = settings.gravity_speed

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
        self._easy_spin_core and self._easy_spin_core.reset()
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
        if self._gravity_core:
            GridUtils.clear_lines(self.grid, lines)
            self._gravity_core.regenerate_grid()
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
            self.trigger_render()
            if not self._easy_spin_core:
                return True
            if TetriminoUtils.can_move(self.tetrimino, self.grid, (0, 1)):
                return True
        if self._wait_easy_spin():
            return True

        for coords, value in self.tetrimino:
            self.grid.set_cell(coords, value)
        self.tetrimino = None
        self.tetrimino_ghost = None

        self._clear_lines() and self._trigger_gravity()

        self.trigger_render()
        return self._spawn_tetrimino()

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
                self.trigger_render()
                time.sleep(self._gravity_speed)
                gravity_runs = True
            if self._clear_lines():
                time.sleep(self._gravity_speed)

    def trigger_render(self):
        self.renderer_core.make_render_request(
            (RenderRequest.full,
                (copy.copy(self.grid),
                    copy.copy(self.tetrimino),
                    copy.copy(self.tetrimino_ghost),
                    copy.copy(self.tetrimino_hold),
                    copy.copy(self.queue))))
