from .grid import Grid
from .core import GameCore
from .timer import GameTimer
from .gravity import GravityCore
from .renderer import RendererCore
from .controller import Controller
from .easy_spin import EasySpinCore
from .generator import GeneratorCore


class Engine:

    def __init__(self, settings):
        grid = self._create_grid(settings)
        generator_core = GeneratorCore(settings)
        easy_spin_core = self._create_easy_spin_core(settings)
        gravity_core = self._create_gravity_core(settings, grid)
        self._timer = GameTimer(settings)
        self._game_core = GameCore(
            settings, grid, (generator_core, gravity_core, easy_spin_core))
        self._controller = Controller(
            (self._game_core, easy_spin_core, self._timer))

    def _create_grid(self, settings):
        return Grid(settings['grid']['width'], settings['grid']['height'])

    def _create_easy_spin_core(self, settings):
        if not settings['easy_spin']['use']:
            return None
        return EasySpinCore(settings)

    def _create_gravity_core(self, settings, grid):
        if not settings['gravity']['use']:
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
