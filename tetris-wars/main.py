import engine.settings as settings
import engine.engine as engine
import engine.renderer as renderer

import threading
import time


def main():
    s = settings.Settings()
    e = engine.Engine(s)
    r = renderer.ConsoleRenderer(e)

    th = threading.Thread(target=e.execute)
    th.start()

    while e.is_running:
        r.render()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
