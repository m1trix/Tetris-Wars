from engine.controller import *
from sdl2 import *


class SdlActionListener(ActionListener):

    def _detect_action(self):
        event = SDL_Event()
        SDL_PollEvent(event)

        if event.type == SDL_KEYUP:
            if event.key.keysym.sym == SDLK_DOWN:
                return Controller.Action.soft_drop_off

        if event.type == SDL_KEYDOWN:
            if event.key.keysym.sym == SDLK_LEFT:
                return Controller.Action.move_left

            if event.key.keysym.sym == SDLK_RIGHT:
                return Controller.Action.move_right

            if event.key.keysym.sym == SDLK_UP:
                return Controller.Action.rotate_clockwise

            if event.key.keysym.sym == SDLK_DOWN:
                return Controller.Action.soft_drop_on

            if event.key.keysym.sym == SDLK_SPACE:
                return Controller.Action.hard_drop
