from threading import Thread
import time
import copy


class RendererCore:

    def __init__(self, game_core):
        self._game_core = game_core

    def get_snapshot(self):
        return (
            copy.copy(self._game_core.grid),
            copy.copy(self._game_core.tetrimino),
            copy.copy(self._game_core.tetrimino_ghost),
            copy.copy(self._game_core.tetrimino_hold)
        )


class Renderer:

    def __init__(self, renderer_core):
        self._renderer_core = renderer_core

    def render(self):
        return

    def _loop(self):
        while self._is_running:
            self.render()
            time.sleep(0.033)

    def start(self):
        self._is_running = True
        Thread(target=self._loop).start()

    def stop(self):
        self._is_running = False
