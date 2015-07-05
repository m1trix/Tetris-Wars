from engine.timer import Timer


class EasySpinEngine:

    def __init__(self, settings):
        self._limit = settings.easy_spin_limit
        self._counter = 0
        self._timer = Timer(settings.easy_spin_timeout)
        self._is_hard_drop = False

    def can_spin(self):
        return self._counter < self._limit

    def is_active(self):
        return self._counter > 0

    def reset(self):
        self._counter = 0

    def add_cycle(self):
        if self.can_spin():
            self._counter += 1
            self._timer.reset()

    def hard_drop(self):
        self._is_hard_drop = True

    def start_countdown(self):
        if self._is_hard_drop:
            self._is_hard_drop = False
            return
        if self.can_spin():
            self._counter += 1
            self._timer.wait()
