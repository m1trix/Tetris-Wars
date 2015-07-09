from .timer import Timer


class EasySpinCore:

    def __init__(self, settings):
        self._limit = settings['easy_spin']['limit']
        self._counter = 0
        self._timer = Timer(settings['easy_spin']['timeout'])
        self._is_hard_drop = False

    def start(self):
        if self._is_hard_drop:
            self._is_hard_drop = False
            return False
        if not self._can_spin():
            return False
        self._timer.start(self._disable_easy_spin)
        return True

    def _disable_easy_spin(self):
        self._counter = self._limit

    def _can_spin(self):
        return self._counter < self._limit

    def is_running(self):
        return self._timer.is_running()

    def reset(self):
        self._counter = 0

    def add_cycle(self):
        if not self._can_spin():
            self._timer.stop()
            return False
        self._counter += 1
        self._timer.reset()
        return True

    def hard_drop(self):
        self._is_hard_drop = True
