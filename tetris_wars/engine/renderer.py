from threading import Thread
from collections import deque
import time
import copy


class RenderRequest:
    full = 'full',
    line_clear = 'line_clear'


class RendererCore:

    def __init__(self, settings, game_core):
        self._game_core = game_core
        self._line_clear_speed = settings.line_clear_speed
        self._render_requests = deque([])

    def make_render_request(self, request):
        type, arguments = request
        if type == RenderRequest.line_clear:
            self._render_requests = deque([])
        self._render_requests.append(request)

    def get_grid_measures(self):
        return self._game_core.grid.measures

    def get_render_request(self):
        if not self._render_requests:
            return None
        return self._render_requests.popleft()

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
