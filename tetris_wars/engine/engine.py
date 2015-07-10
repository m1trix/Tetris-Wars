from .core import GameCore
from .timer import GameTimer
from .renderer import RendererCore
from .controller import Controller
from .renderer import RendererClient


class Engine:

    def __init__(self, settings):
        self._settings = settings
        self._renderer_client = RendererClient()
        self._timer = GameTimer(settings)
        self._game_core = GameCore(settings, self._renderer_client)
        self._controller = Controller(
            self._game_core, self._timer, self._renderer_client)

    def execute(self):
        self._is_running = True
        while self._is_running:
            self._timer.start().wait()
            self._is_running = self._game_core.do_progress()

    @property
    def controller(self):
        return self._controller

    @property
    def renderer_core(self):
        return RendererCore(
            self._settings, self._renderer_client, self._game_core.view)
