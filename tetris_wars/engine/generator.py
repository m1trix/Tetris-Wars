import copy
from random import randint
from collections import deque
from .tetrimino import *
from .statistics import StatisticsCore


class GeneratorCore:

    def __init__(self, settings):
        self._repeat_limit = max(2, settings['generator']['repetition_limit'])
        self._queue_size = max(0, settings['generator']['queue_size'])
        self._statistics_core = StatisticsCore()
        self._statistics_core.reset()
        self._last_tetriminos = deque([])
        self._queue = None
        if self._queue_size > 0:
            self._queue = deque([])
            self._fill_queue()

    def _fill_queue(self):
        for i in range(self._queue_size):
            self._queue.append(self._spawn_tetrimino())

    @property
    def view(self):
        return GeneratorVeiw(self)

    @property
    def statistics_core(self):
        return self._statistics_core

    @property
    def queue(self):
        if not self._queue:
            return []
        return (x for x in self._queue)

    def generate_tetrimino(self):
        tetrimino = self._spawn_tetrimino()
        if self._queue:
            self._queue.append(tetrimino)
            tetrimino = self._queue.popleft()
        self._statistics_core.note_tetrimino_spawn(tetrimino)
        return tetrimino

    def _create_random_tetrimino(self):
        types = list(Tetrimino.Type)
        type = types[randint(0, len(types) - 1)]
        return create_tetrimino(type, 0, 0)

    def _spawn_tetrimino(self):
        tetrimino = None
        while True:
            tetrimino = self._create_random_tetrimino()
            if (self._last_tetriminos.count(tetrimino.type)
                    < self._repeat_limit):
                break
        self._last_tetriminos.append(tetrimino.type)
        if len(self._last_tetriminos) > self._repeat_limit:
            self._last_tetriminos.popleft()
        return tetrimino


class GeneratorVeiw:

    def __init__(self, generator_core):
        self._generator_core = generator_core
        self._statistics_view = generator_core.statistics_core.view

    @property
    def statistics_view(self):
        return self._statistics_view

    @property
    def queue(self):
        return self._generator_core.queue
