from engine.action import Action
from engine.controller import ActionListener


class ConsoleActionListener(ActionListener):

    def _detect_action(self):
        symbol = input()

        if symbol == 'a':
            return Action.move_left

        if symbol == 'd':
            return Action.move_right

        if symbol == 'w':
            return Action.rotate_clockwise

        if symbol == ' ':
            return Action.hard_drop
