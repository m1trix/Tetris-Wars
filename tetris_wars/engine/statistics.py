from .tetrimino import Tetrimino


class StatisticsCore:

    def __init__(self):
        self.reset()

    def reset(self):
        self._score = 0
        self._statistics = dict(map(
            lambda x: (x, 0),
            list(Tetrimino.Type)))
        self._is_tetris_sqored = False

    @property
    def score(self):
        return self._score

    @property
    def statistics(self):
        return list(self._statistics.items())

    @property
    def view(self):
        return StatisticsView(self)

    def note_tetrimino_spawn(self, tetrimino):
        self._statistics[tetrimino.type] += 1

    def note_lines_clear(self, count):
        if count < 4:
            self._is_tetris_scored = False
            self._score += count * 100
            return
        if not self._is_tetris_scored:
            self._score += 800
            self._is_tetris_scored = True
            return
        self._score += 1200


class StatisticsView:

    def __init__(self, statistics_core):
        self._statistics_core = statistics_core

    @property
    def score(self):
        return self._statistics_core.score

    @property
    def statistics(self):
        return self._statistics_core.statistics
