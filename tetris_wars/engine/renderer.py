import time
import copy
from enum import Enum
from threading import Thread
from collections import deque
from .grid import ImmutableGrid


class RenderRequest(Enum):
    full = 'full',
    line_clear = 'line_clear',
    cannot_hold = 'cannot_hold'


class RendererCore:

    def __init__(self, settings, game_core, generator_core):
        self.grid = ImmutableGrid(game_core.grid)
        self._game_core = game_core
        self._generator = generator_core
        self._line_clear_speed = settings.line_clear_speed
        self._requests_count = len(list(RenderRequest))
        self._render_requests = [None] * self._requests_count
        self._priorities = {
            RenderRequest.full: 2,
            RenderRequest.cannot_hold: 1,
            RenderRequest.line_clear: 0
        }

    @property
    def statistics_core(self):
        return self._game_core.statistics_core.view

    def get_tetrimino(self):
        return (self._game_core.tetrimino
                and self._game_core.tetrimino.immutable())

    def get_tetrimino_ghost(self):
        return (self._game_core.tetrimino_ghost
                and self._game_core.tetrimino_ghost.immutable())

    def get_tetrimino_hold(self):
        return (self._game_core.tetrimino_hold
                and self._game_core.tetrimino_hold.immutable())

    def get_generator_core(self):
        return self._generator

    def make_render_request(self, type, arguments=None):
        priority = self._priorities[type]
        self._render_requests[priority] = (type, arguments)

    def get_render_request(self):
        for i in range(self._requests_count):
            if self._render_requests[i]:
                request = self._render_requests[i]
                self._render_requests[i] = None
                return request
        return None

    @property
    def line_clear_speed(self):
        return self._line_clear_speed


class Renderer:

    def __init__(self, renderer_core):
        self._renderer_core = renderer_core
        self._sleep_time = 0.0333

    def render(self, request):
        return

    def _loop(self):
        while self._is_running:
            request = self._renderer_core.get_render_request()
            if request:
                self.render(request)
            time.sleep(self._sleep_time)

    def start(self):
        self._is_running = True
        Thread(target=self._loop).start()

    def stop(self):
        self._is_running = False
