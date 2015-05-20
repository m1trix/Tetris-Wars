from engine.action import Action
from engine.controller import ActionListener
from sdl2 import *


class SdlActionListener(ActionListener):

    def __init__(self, control_unit):
        super(SdlActionListener, self).__init__(control_unit)
        self._key_left = False
        self._key_right = False
        self._key_down = False

    def _detect_actions(self):
        event = SDL_Event()
        while(SDL_PollEvent(event)):
            if event.type == SDL_KEYUP:
                if event.key.keysym.sym == SDLK_LEFT:
                    self._key_left = False
                elif event.key.keysym.sym == SDLK_RIGHT:
                    self._key_right = False
                elif event.key.keysym.sym == SDLK_DOWN:
                    self._key_down = False
                    yield Action.soft_drop_off

            elif event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_LEFT:
                    self._key_left = True

                elif event.key.keysym.sym == SDLK_RIGHT:
                    self._key_right = True

                elif event.key.keysym.sym == SDLK_UP:
                    yield Action.rotate_clockwise

                elif event.key.keysym.sym == SDLK_DOWN:
                    if not self._key_down:
                        self._key_down = True
                        yield Action.soft_drop_on

                elif event.key.keysym.sym == SDLK_SPACE:
                    yield Action.hard_drop

        if self._key_left:
            yield Action.move_left
        if self._key_right:
            yield Action.move_right
