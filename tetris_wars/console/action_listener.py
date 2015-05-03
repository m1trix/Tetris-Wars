from engine.controller import *


class ConsoleActionListener(ActionListener):

    def _detect_action(self):
        symbol = input()

        if symbol == 'a':
            return Controller.Action.move_left

        if symbol == 'd':
            return Controller.Action.move_right

        if symbol == 'w':
            return Controller.Action.rotate_clockwise

        if symbol == ' ':
            return Controller.Action.hard_drop
