from engine.settings import Settings
from engine.engine import Engine
from graphics.sdl_renderer import SdlRenderer
from graphics.sdl_listener import SdlActionListener

import threading
import time


def main():
    s = Settings()
    r = SdlRenderer()
    e = Engine(s, r)
    c = SdlActionListener(e.controller)

    c.start()
    e.execute()

if __name__ == "__main__":
    main()
