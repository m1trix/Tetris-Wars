import time
import copy
from enum import Enum
from threading import Thread
from collections import deque


class RenderRequest(Enum):
    full = 'full',
    line_clear = 'line_clear',
    cannot_hold = 'cannot_hold'


class RenderAnimation:

    def __init__(self, requests, index):
        self._requests = requests
        self._index = index

    def wait(self):
        while self._requests[self._index]:
            time.sleep(0.001)


class RendererClient:

    def __init__(self):
        self._requests_count = len(list(RenderRequest))
        self._render_requests = [None] * self._requests_count
        self._priorities = {
            RenderRequest.full: 2,
            RenderRequest.cannot_hold: 1,
            RenderRequest.line_clear: 0
        }

    def request(self, type, arguments=None):
        priority = self._priorities[type]
        self._render_requests[priority] = (type, arguments)
        return RenderAnimation(self._render_requests, priority)

    def pop_next_request(self):
        for i in range(self._requests_count):
            if self._render_requests[i]:
                request = self._render_requests[i]
                self._render_requests[i] = None
                return request
        return None


class RendererCore:

    def __init__(self, settings, renderer_client, game_view):
        self._renderer_client = renderer_client
        self._game_view = game_view
        self._line_clear_speed = settings['game']['line_clear_speed']

    @property
    def renderer_client(self):
        return self._renderer_client

    @property
    def game_view(self):
        return self._game_view


class Renderer:

    def __init__(self, renderer_core):
        self._renderer_client = renderer_core.renderer_client
        self._game_view = renderer_core.game_view
        self._line_clear_speed = renderer_core._line_clear_speed
        self._sleep_time = 1 / 30

    def render(self, request):
        return

    def _loop(self):
        while self._is_running:
            request = self._renderer_client.pop_next_request()
            if request:
                self.render(request)
            time.sleep(self._sleep_time)

    def start(self):
        self._is_running = True
        Thread(target=self._loop).start()

    def stop(self):
        self._is_running = False
