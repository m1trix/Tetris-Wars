from enum import Enum
from engine.tetrimino import Rotation
from threading import Thread


class Controller:

    class Action(Enum):
        move_left = 'move_left'
        move_right = 'move_right'

        hard_drop = 'hard_drop'
        soft_drop_on = 'soft_drop_on'
        soft_drop_off = 'soft_drop_off'

        rotate_clockwise = 'rotate_clockwise'
        rotate_counterclockwise = 'rotate_counterclockwise'

    def do_action(self, action):
        pass


class ActionListener:

    def __init__(self, controller):
        self.__controller = controller
        self.__is_running = False

    def _detect_action(self):
        pass

    def __loop(self):
        self.__is_running = True
        while self.__is_running:
            action = self._detect_action()
            self.__controller.do_action(action)

    def start(self):
        thread = Thread(target=self.__loop)
        thread.start()

    def stop(self):
        self.__is_running = False
