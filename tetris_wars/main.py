from engine.settings import Settings
from engine.engine import Engine
from graphics.sdl_renderer import SdlRenderer
from graphics.sdl_listener import SdlActionListener
import threading
import time


def main():
    e = Engine(Settings())
    r = SdlRenderer(e.renderer_core)
    c = SdlActionListener(e.controller)

    c.start()
    r.start()

    e.execute()

    r.stop()
    c.stop()

if __name__ == "__main__":
    main()
