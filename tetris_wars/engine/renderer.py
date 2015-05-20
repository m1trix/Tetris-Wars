from threading import Thread
import time


class Renderer:

    def set_render_unit(self, render_unit):
        self._render_unit = render_unit

    def render(self):
        return

    def _loop(self):
        while self._is_running:
            self.render()
            time.sleep(0.033)

    def start(self):
        self._is_running = True
        Thread(target=self._loop).start()

    def stop(self):
        self._is_running = False
