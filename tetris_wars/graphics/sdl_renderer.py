from sdl2 import *
from sdl2.ext import Window
from sdl2.ext import Color
from sdl2.ext import fill
from engine.renderer import Renderer
from engine.tetrimino import Tetrimino
from engine.tetrimino import TetriminoUtils


GRID_X_OFFSET = 6
GRID_Y_OFFSET = 1
SQUARE_SIZE = 16
GRID_COLOR = Color(0, 64, 64, 64)


class SdlRenderer(Renderer):

    def __init__(self, renderer_core):
        super(SdlRenderer, self).__init__(renderer_core)
        SDL_Init(SDL_INIT_VIDEO)
        self._calculate_window_size()
        self._window = Window(
            'Tetris Wars',
            self._screen_measures)
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

    def _calculate_window_size(self):
        w, h = self._renderer_core.get_snapshot()[0].measures
        self._screen_measures = (
            (w + GRID_X_OFFSET + 1) * SQUARE_SIZE,
            (h + GRID_Y_OFFSET + 1) * SQUARE_SIZE)

    def _render_frame(self):
        w, h = self._screen_measures
        SDL_FillRect(
            self._surface,
            SDL_Rect(0, 0, w, h),
            Color(0, 0, 0, 0))

    def _render_hold(self, hold):
        SDL_FillRect(
            self._surface,
            SDL_Rect(
                SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE * 4,
                SQUARE_SIZE * 4),
            Color(0, 16, 16, 16))
        if not hold:
            return
        x, y, w, h = TetriminoUtils.calculate_actual_measures(hold)
        ox, oy = (((4 - w - 2 * x) * SQUARE_SIZE) // 2,
                  ((4 - h - 2 * y) * SQUARE_SIZE) // 2)
        for ((x, y), value) in hold:
            SDL_FillRect(
                self._surface,
                SDL_Rect(
                    ox + (1 + x) * SQUARE_SIZE,
                    oy + (1 + y) * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE),
                self._colors[value])

    def render(self):
        self._render_frame()
        grid, tetrimino, ghost, hold = self._renderer_core.get_snapshot()
        w, h = grid.measures
        self._render_hold(hold)
        for y in range(h):
            for x in range(w):
                if tetrimino.get_cell((x, y)):
                    color = self._colors[tetrimino.get_cell((x, y))]
                elif ghost.get_cell((x, y)):
                    color = Color(0, 64, 64, 64)
                elif grid.get_cell((x, y)):
                    color = self._colors[grid.get_cell((x, y))]
                else:
                    color = Color(0, 16, 16, 16)

                SDL_FillRect(
                    self._surface,
                    SDL_Rect(
                        (x + GRID_X_OFFSET) * SQUARE_SIZE,
                        (y + GRID_Y_OFFSET) * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE),
                    color)
        self._window.refresh()
