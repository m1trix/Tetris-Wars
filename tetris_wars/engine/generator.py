import copy
from random import randint
from collections import deque
from .tetrimino import *
from .statistics import StatisticsCore


class GeneratorCore:

    def __init__(self, settings):
        self._repeat_limit = max(2, settings.tetrimino_repetition_limit)
        self._queue_size = max(0, settings.queue_size)
        self._statistics_core = StatisticsCore()
        self.reset()

    def reset(self):
        self._statistics_core.reset()
        self._last_tetriminos = deque([])
        self._queue = None
        if self._queue_size > 0:
            self._queue = deque([])
            self._fill_queue()

    @property
    def statistics_core(self):
        return self._statistics_core

    @property
    def queue(self):
        if not self._queue:
            return []
        return copy.copy(self._queue)

    def _fill_queue(self):
        for i in range(self._queue_size):
            self._queue.append(self._spawn_tetrimino())

    def generate_tetrimino(self):
        tetrimino = self._spawn_tetrimino()
        if self._queue:
            self._queue.append(tetrimino)
            tetrimino = self._queue.popleft()
        self._statistics_core.note_tetrimino_spawn(tetrimino)
        return tetrimino

    def _spawn_tetrimino(self):
        is_repeated = True
        tetrimino = None
        while is_repeated:
            types = list(Tetrimino.Type)
            type = types[randint(0, len(types) - 1)]
            tetrimino = create_tetrimino(type, 0, 0)
            if not self._last_tetriminos:
                is_repeated = False
            for t in self._last_tetriminos:
                if t.type != tetrimino.type:
                    is_repeated = False
                    break
        self._last_tetriminos.append(tetrimino)
        if len(self._last_tetriminos) > self._repeat_limit:
            self._last_tetriminos.popleft()
        return tetrimino
