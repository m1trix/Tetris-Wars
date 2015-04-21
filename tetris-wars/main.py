from engine.settings import Settings
from engine.engine import Engine
from console.console_renderer import ConsoleRenderer

import threading
import time


def main():
    s = Settings()
    r = ConsoleRenderer()
    e = Engine(s, r)

    e.execute()

if __name__ == "__main__":
    main()
