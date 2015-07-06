from engine.timer import GameTimer
from engine.easy_spin import EasySpinCore
from engine.core import GameCore
from engine.renderer import RendererCore
from engine.controller import Controller
from engine.grid import Grid
from engine.gravity import GravityCore


class Engine:

    def __init__(self, settings):
        grid = self._create_grid(settings)
        easy_spin_core = self._create_easy_spin_core(settings)
        gravity_core = self._create_gravity_core(settings, grid)
        self._timer = GameTimer(settings)
        self._game_core = GameCore(settings, grid, easy_spin_core, gravity_core)
        self._controller = Controller((self._game_core, easy_spin_core, self._timer))

    def _create_grid(self, settings):
        return Grid(settings.grid_width, settings.grid_height)

    def _create_easy_spin_core(self, settings):
        if not settings.use_easy_spin:
            return None
        return EasySpinCore(settings)

    def _create_gravity_core(self, settings, grid):
        if not settings.use_gravity:
            return None
        return GravityCore(grid)

    def _progress_game(self):
        self._timer.start().wait()
        self._is_running = self._game_core.do_progress()

    def execute(self):
        self._is_running = True
        while self._is_running:
            self._progress_game()

    @property
    def controller(self):
        return self._controller

    @property
    def renderer_core(self):
        return self._game_core.renderer_core
