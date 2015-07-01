from sdl2 import *
from sdl2.ext import Window
from sdl2.ext import Color
from sdl2.ext import fill
from engine.renderer import Renderer
from engine.tetrimino import Tetrimino


class SdlRenderer(Renderer):

    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO)
        self._window = Window(
            'Tetris Wars',
            (160, 320))
        self._window.show()
        self._window.refresh()
        self._surface = self._window.get_surface()
        self._colors = {
            Tetrimino.Type.I: Color(0, 0, 255, 255),
            Tetrimino.Type.J: Color(0, 0, 0, 255),
            Tetrimino.Type.L: Color(0, 255, 128, 0),
            Tetrimino.Type.O: Color(0, 255, 255, 0),
            Tetrimino.Type.S: Color(0, 0, 255, 128),
            Tetrimino.Type.T: Color(0, 128, 0, 128),
            Tetrimino.Type.Z: Color(0, 200, 0, 0)
        }

    def render(self):
        grid, tetrimino, ghost = self._renderer_core.get_snapshot()
        w, h = grid.measures
        for y in range(h):
            for x in range(w):
                if tetrimino.get_cell((x, y)):
                    color = self._colors[tetrimino.get_cell((x, y))]
                elif ghost.get_cell((x, y)):
                    color = Color(0, 32, 32, 32)
                elif grid.get_cell((x, y)):
                    color = self._colors[grid.get_cell((x, y))]
                else:
                    color = Color(0, 0, 0, 0)

                SDL_FillRect(
                    self._surface,
                    SDL_Rect(x * 16, y * 16, x * 16 + 16, y * 16 + 16),
                    color)
        self._window.refresh()
