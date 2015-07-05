import time


class Timer():

    def __init__(self, timeout):
        self._timer = 0
        self._timeout = timeout

    def reset(self):
        self._timer = int(self._timeout * 1000)

    def turn_off(self):
        self._timer = 0

    def wait(self):
        self.reset()
        while self._timer > 0:
            self._timer -= 1
            time.sleep(0.001)


class GameTimer(Timer):

    def __init__(self, settings):
        super(GameTimer, self).__init__(settings.game_speed)
        self._game_speed = settings.game_speed
        self._soft_drop_speed = settings.soft_drop_speed

    def soft_drop_on(self):
        self._timeout = self._soft_drop_speed
        self.reset()

    def soft_drop_off(self):
        self._timeout = self._game_speed
        self.reset()
