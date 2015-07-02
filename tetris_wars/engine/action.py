from enum import Enum


class Action(Enum):
    move_left = 'move_left'
    move_right = 'move_right'

    hard_drop = 'hard_drop'
    soft_drop_on = 'soft_drop_on'
    soft_drop_off = 'soft_drop_off'

    rotate_clockwise = 'rotate_clockwise'
    rotate_counterclockwise = 'rotate_counterclockwise'

    hold = 'hold'
