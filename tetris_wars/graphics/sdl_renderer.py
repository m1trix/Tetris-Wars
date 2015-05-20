from sdl2 import *
from sdl2.ext import Window
from sdl2.ext import Color
from sdl2.ext import fill
from engine.renderer import Renderer


class SdlRenderer(Renderer):

    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO)
        self._window = Window(
            'Tetris Wars',
            (160, 320))
        self._window.show()
        self._window.refresh()
        self._surface = self._window.get_surface()

    def render(self):
        grid, tetrimino, ghost = self._render_unit.get_snapshot()
        w, h = grid.measures
        for y in range(h):
            for x in range(w):
                if tetrimino.get_cell((x, y)):
                    color = Color(0, 128, 128, 128)
                elif ghost.get_cell((x, y)):
                    color = Color(0, 32, 32, 32)
                elif grid.get_cell((x, y)):
                    color = Color(0, 128, 128, 128)
                else:
                    color = Color(0, 0, 0, 0)

                SDL_FillRect(
                    self._surface,
                    SDL_Rect(x * 16, y * 16, x * 16 + 16, y * 16 + 16),
                    color)
        self._window.refresh()
