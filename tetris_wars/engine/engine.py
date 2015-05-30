from engine.timer import Timer
from engine.core import GameCore
from engine.renderer import RendererCore
from engine.controller import Controller


class Engine:

    def __init__(self, settings):
        self._timer = Timer(settings)
        self._game_core = GameCore(settings)
        self._renderer_core = RendererCore(self._game_core)
        self._controller = Controller(self._game_core, self._timer)

    def _progress_game(self):
        self._timer.wait()
        self._game_core.do_progress()

    def execute(self):
        self._is_running = True
        self._game_core._spawn_tetrimino()
        while self._is_running:
            self._progress_game()

    @property
    def controller(self):
        return self._controller

    @property
    def renderer_core(self):
        return self._renderer_core
