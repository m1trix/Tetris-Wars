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
COMPACT_SQUARE_SIZE = 12

BORDER_COLOR = Color(0, 0, 21, 27)
GRID_COLOR = Color(0, 0, 21, 27)
GHOST_COLOR = Color(0, 7, 54, 66)


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
        self._background_color = Color(0, 0, 10, 15)
        self._colors = {
            Tetrimino.Type.I: Color(0, 42, 161, 152),
            Tetrimino.Type.J: Color(0, 38, 139, 210),
            Tetrimino.Type.L: Color(0, 203, 75, 22),
            Tetrimino.Type.O: Color(0, 181, 137, 0),
            Tetrimino.Type.S: Color(0, 133, 153, 0),
            Tetrimino.Type.T: Color(0, 211, 54, 130),
            Tetrimino.Type.Z: Color(0, 220, 50, 47)
        }

    def _calculate_window_size(self):
        w, h = self._renderer_core.get_snapshot()[0].measures
        self._screen_measures = (
            (w + GRID_X_OFFSET + 6) * SQUARE_SIZE,
            (h + GRID_Y_OFFSET + 1) * SQUARE_SIZE)
        self._queue_offset = (w + GRID_X_OFFSET + 1, GRID_Y_OFFSET)

    def _render_frame(self):
        w, h = self._screen_measures
        SDL_FillRect(
            self._surface,
            SDL_Rect(0, 0, w, h),
            self._background_color)

    def _render_hold(self, tetrimino):
        SDL_FillRect(
            self._surface,
            SDL_Rect(
                SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE * 4,
                SQUARE_SIZE * 4),
            GRID_COLOR)
        if not tetrimino:
            return
        x, y, w, h = TetriminoUtils.calculate_actual_measures(tetrimino)
        ox, oy = (((4 - w - 2 * x) * SQUARE_SIZE) // 2,
                  ((4 - h - 2 * y) * SQUARE_SIZE) // 2)
        for ((x, y), value) in tetrimino:
            sx, sy = (ox + (1 + x) * SQUARE_SIZE,
                      oy + (1 + y) * SQUARE_SIZE)
            self._smart_render(tetrimino, (x, y), (sx, sy), None, SQUARE_SIZE)

    def _render_queue(self, queue):
        oqx, oqy = self._queue_offset
        i = 0
        for tetrimino in queue:
            SDL_FillRect(
                self._surface,
                SDL_Rect(
                    oqx * SQUARE_SIZE,
                    (oqy + 4 * i) * SQUARE_SIZE,
                    SQUARE_SIZE * 3,
                    SQUARE_SIZE * 3),
                GRID_COLOR)
            x, y, w, h = TetriminoUtils.calculate_actual_measures(tetrimino)
            ox, oy = (((4 - w - 2 * x) * COMPACT_SQUARE_SIZE) // 2,
                      ((4 - h - 2 * y) * COMPACT_SQUARE_SIZE) // 2)
            for ((x, y), value) in tetrimino:
                sx, sy = (oqx * SQUARE_SIZE + ox + x * COMPACT_SQUARE_SIZE,
                          (oqy + 4 * i) * SQUARE_SIZE + oy + y * COMPACT_SQUARE_SIZE)
                self._smart_render(tetrimino, (x, y), (sx, sy), None, COMPACT_SQUARE_SIZE)
            i += 1

    def _render_tetrimino_square(self, x, y, color, square_size):
        SDL_FillRect(
            self._surface,
            SDL_Rect(x + 1, y + 1, square_size - 1, square_size - 1),
            color)

    def _smart_render(self, grid, grid_coords, screen_coords, color, square_size):
        x, y = grid_coords
        gw, gh = grid.measures
        sx, sy = screen_coords
        segment = grid.get_cell(grid_coords)
        color = color or self._colors[segment.get_type()]

        xfr, yfr, w, h = sx + 1, sy + 1, square_size - 1, square_size - 1
        SDL_FillRect(
            self._surface,
            SDL_Rect(xfr, yfr, w, h),
            color)
        if x > 0 and grid.get_cell((x - 1, y)) and grid.get_cell((x - 1, y)) == segment:
            SDL_FillRect(self._surface, SDL_Rect(xfr - 1, yfr, 1, h), color)
        if y > 0 and grid.get_cell((x, y - 1)) and grid.get_cell((x, y - 1)) == segment:
            SDL_FillRect(self._surface, SDL_Rect(xfr, yfr - 1, w, 1), color)

    def render(self):
        self._render_frame()
        snapshot = self._renderer_core.get_snapshot()
        grid, tetrimino, ghost, hold, queue = snapshot
        w, h = grid.measures
        self._render_hold(hold)
        self._render_queue(queue)
        SDL_FillRect(
            self._surface,
            SDL_Rect(
                GRID_X_OFFSET * SQUARE_SIZE,
                GRID_Y_OFFSET * SQUARE_SIZE,
                w * SQUARE_SIZE,
                h * SQUARE_SIZE),
            GRID_COLOR)
        for y in range(h):
            for x in range(w):
                sx, sy = ((x + GRID_X_OFFSET) * SQUARE_SIZE,
                          (y + GRID_Y_OFFSET) * SQUARE_SIZE)
                if tetrimino and tetrimino.get_cell((x, y)):
                    self._smart_render(tetrimino, (x, y), (sx, sy), None, SQUARE_SIZE)
                elif ghost and ghost.get_cell((x, y)):
                    self._smart_render(ghost, (x, y), (sx, sy), GHOST_COLOR, SQUARE_SIZE)
                elif grid.get_cell((x, y)):
                    self._smart_render(grid, (x, y), (sx, sy), None, SQUARE_SIZE)
        self._window.refresh()
