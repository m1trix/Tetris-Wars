import time


class Timer:

    def __init__(self, settings):
        self._normal_speed = settings.game_speed
        self._soft_drop_speed = settings.soft_drop_time
        self._game_speed = self._normal_speed
        self._timer = self._game_speed

    def soft_drop_on(self):
        self._game_speed = self._soft_drop_speed
        self.reset()

    def soft_drop_off(self):
        self._game_speed = self._normal_speed
        self.reset()

    def reset(self):
        self._timer = 0

    def wait(self):
        self._timer = int(self._game_speed * 1000)
        while self._timer > 0:
            self._timer -= 1
            time.sleep(0.001)
