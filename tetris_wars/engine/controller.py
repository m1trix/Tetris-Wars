from threading import Thread
import time


class ActionListener:

    def __init__(self, control_unit):
        self._control_unit = control_unit
        self._is_running = False

    def _detect_action(self):
        pass

    def _loop(self):
        self._is_running = True
        while self._is_running:
            action = self._detect_action()
            self._control_unit.do_action(action)
            time.sleep(0.01)

    def start(self):
        thread = Thread(target=self._loop)
        thread.start()

    def stop(self):
        self._is_running = False
