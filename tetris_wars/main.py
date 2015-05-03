from engine.settings import Settings
from engine.engine import Engine
from console.console_renderer import ConsoleRenderer
from console.action_listener import ConsoleActionListener

import threading
import time


def main():
    s = Settings()
    r = ConsoleRenderer()
    e = Engine(s, r)
    c = ConsoleActionListener(e.controller)

    c.start()
    e.execute()

if __name__ == "__main__":
    main()
