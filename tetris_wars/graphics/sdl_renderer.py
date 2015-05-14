from sdl2 import *
from sdl2.ext import Window
from sdl2.ext import Color
from sdl2.ext import fill
from engine.renderer import Renderer


class SdlRenderer(Renderer):

    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO)
        self.__window = Window(
            'Tetris Wars',
            (160, 320))
        self.__window.show()
        self.__window.refresh()
        self.__surface = self.__window.get_surface()

    def render(self):
        w, h = self._engine.measures
        for y in range(h):
            for x in range(w):
                color = Color(0, 0, 0, 0)
                b = self._engine.tetrimino
                b = b and self._engine.tetrimino.get_cell((x, y))

                b = b or self._engine.grid.get_cell((x, y))
                color = b and Color(0, 128, 128, 128) or color

                if not b and self._engine.ghost:
                    b = self._engine.ghost.get_cell((x, y))
                    color = b and Color(0, 32, 32, 32) or color

                SDL_FillRect(self.__surface, SDL_Rect(x * 16, y * 16, x * 16 + 16, y * 16 + 16), color)
        self.__window.refresh()

    def clear_lines(self, range):
        return

# TODO PEP-8
