import time
from threading import Thread


class Timer():

    def __init__(self, timeout):
        self._timer = 0
        self._timeout = timeout
        self._thread = None

    def reset(self):
        self._timer = int(self._timeout * 1000)
        return self

    def stop(self):
        self._timer = 0
        return self

    def _countdown(self):
        self.reset()
        while self._timer > 0:
            self._timer -= 1
            time.sleep(0.001)
        self._thread = None
        if self._on_finish:
            self._on_finish()
            self._on_finish = None

    def start(self, on_finish=None):
        self._on_finish = on_finish
        self._thread = Thread(target=self._countdown)
        self._thread.start()
        return self

    def wait(self):
        if self._thread:
            self._thread.join()

    def is_running(self):
        return self._thread is not None


class GameTimer(Timer):

    def __init__(self, settings):
        super(GameTimer, self).__init__(settings['game']['speed'])
        self._game_speed = settings['game']['speed']
        self._soft_drop_speed = settings['game']['soft_drop_speed']

    def soft_drop_on(self):
        self._timeout = self._soft_drop_speed
        self.reset()

    def soft_drop_off(self):
        self._timeout = self._game_speed
        self.reset()
