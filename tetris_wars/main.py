from engine.settings import Settings
from engine.engine import Engine
from graphics.sdl_renderer import SdlRenderer
from graphics.sdl_listener import SdlActionListener
import threading
import time


def main():
    e = Engine(Settings())
    r = SdlRenderer()
    r.set_render_unit(e.render_unit)
    c = SdlActionListener(e.control_unit)

    r.start()
    c.start()

    e.execute()

    c.stop()
    r.stop()

if __name__ == "__main__":
    main()
