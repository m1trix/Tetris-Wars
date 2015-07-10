import os
import time
from sdl2 import *
from sdl2.ext import Window
from sdl2.ext import Color
from sdl2.ext import fill
from engine.renderer import Renderer
from engine.renderer import RenderRequest
from engine.tetrimino import Tetrimino
from engine.tetrimino import TetriminoUtils


GRID_X_OFFSET = 6
GRID_Y_OFFSET = 1
SQUARE_SIZE = 16
COMPACT_SQUARE_SIZE = 12

BORDER_COLOR = Color(0, 0, 21, 27)
GRID_COLOR = Color(0, 0, 21, 27)
GHOST_COLOR = Color(0, 7, 54, 66)
LINE_CLEAR_COLOR = Color(0, 238, 232, 213)


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
        self._draw_statistics()
        self._full_render()

    def _calculate_window_size(self):
        w, h = self._game_view.grid.measures
        self._screen_measures = (
            (w + GRID_X_OFFSET + 6) * SQUARE_SIZE,
            (h + GRID_Y_OFFSET + 1) * SQUARE_SIZE)
        self._queue_offset = (w + GRID_X_OFFSET + 1, GRID_Y_OFFSET)

    def _draw_frame(self):
        w, h = self._screen_measures
        SDL_FillRect(
            self._surface,
            SDL_Rect(0, 0, w, h),
            self._background_color)

    def _draw_hold(self, background=GRID_COLOR):
        tetrimino = self._game_view.held_tetrimino
        SDL_FillRect(
            self._surface,
            SDL_Rect(
                SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE * 4,
                SQUARE_SIZE * 4),
            background)
        if not tetrimino:
            return
        x, y, w, h = TetriminoUtils.calculate_actual_measures(tetrimino)
        ox, oy = (((4 - w - 2 * x) * SQUARE_SIZE) // 2,
                  ((4 - h - 2 * y) * SQUARE_SIZE) // 2)
        for x, y, value in tetrimino:
            sx, sy = (ox + (1 + x) * SQUARE_SIZE,
                      oy + (1 + y) * SQUARE_SIZE)
            self._draw_tetrimino(tetrimino, (x, y), (sx, sy), SQUARE_SIZE)

    def _draw_queue(self):
        queue = self._game_view.generator_view.queue
        if not queue:
            return
        oqx, oqy = self._queue_offset
        i = 0
        for tetrimino in queue:
            SDL_FillRect(
                self._surface,
                SDL_Rect(oqx * SQUARE_SIZE,
                         (oqy + 4 * i) * SQUARE_SIZE,
                         SQUARE_SIZE * 3,
                         SQUARE_SIZE * 3),
                GRID_COLOR)
            x, y, w, h = TetriminoUtils.calculate_actual_measures(tetrimino)
            ox, oy = (((4 - w - 2 * x) * COMPACT_SQUARE_SIZE) // 2,
                      ((4 - h - 2 * y) * COMPACT_SQUARE_SIZE) // 2)
            for x, y, value in tetrimino:
                offset_x = oqx * SQUARE_SIZE + ox
                offset_y = (oqy + 4 * i) * SQUARE_SIZE + oy
                sx = offset_x + x * COMPACT_SQUARE_SIZE
                sy = offset_y + y * COMPACT_SQUARE_SIZE
                self._draw_tetrimino(
                    tetrimino, (x, y), (sx, sy), COMPACT_SQUARE_SIZE)
            i += 1

    def _draw_tetrimino(
            self, grid, grid_coords, screen_coords, square_size, color=None):
        x, y = grid_coords
        gw, gh = grid.measures
        sx, sy = screen_coords
        segment = grid.get_cell(x, y)
        color = color or self._colors[segment.type]

        xfr, yfr, w, h = sx + 1, sy + 1, square_size - 1, square_size - 1
        SDL_FillRect(self._surface, SDL_Rect(xfr, yfr, w, h), color)
        if x > 0 and grid.get_cell(x - 1, y) == segment:
            SDL_FillRect(self._surface, SDL_Rect(xfr - 1, yfr, 1, h), color)
        if y > 0 and grid.get_cell(x, y - 1) == segment:
            SDL_FillRect(self._surface, SDL_Rect(xfr, yfr - 1, w, 1), color)

    def _draw_grid(self):
        w, h = self._game_view.grid.measures
        tetrimino = self._game_view.falling_tetrimino
        ghost = self._game_view.ghost_tetrimino
        SDL_FillRect(
            self._surface,
            SDL_Rect(GRID_X_OFFSET * SQUARE_SIZE,
                     GRID_Y_OFFSET * SQUARE_SIZE,
                     w * SQUARE_SIZE,
                     h * SQUARE_SIZE),
            GRID_COLOR)
        for y in range(h):
            for x in range(w):
                sx, sy = ((x + GRID_X_OFFSET) * SQUARE_SIZE,
                          (y + GRID_Y_OFFSET) * SQUARE_SIZE)

                if tetrimino and tetrimino.get_cell(x, y):
                    self._draw_tetrimino(
                        tetrimino, (x, y), (sx, sy), SQUARE_SIZE)

                elif ghost and ghost.get_cell(x, y):
                    self._draw_tetrimino(
                        ghost, (x, y), (sx, sy), SQUARE_SIZE, GHOST_COLOR)

                elif self._game_view.grid.get_cell(x, y):
                    self._draw_tetrimino(
                        self._game_view.grid, (x, y), (sx, sy), SQUARE_SIZE)

    def _draw_statistics(self):
        os.system("clear")
        print("STATISTICS:")
        statistics_view = self._game_view.generator_view.statistics_view
        for key, value in statistics_view.statistics:
            print("{}: {}".format(key, value))
        print("\nSCORE:%06d" % statistics_view.score)

    def _full_render(self):
        self._draw_frame()
        self._draw_hold()
        self._draw_queue()
        self._draw_grid()
        self._draw_statistics()
        self._window.refresh()

    def _animate_cannot_hold(self, arguments):
        w, h = self._game_view.grid.measures
        sleep_time = 0.1
        colors = [
            GRID_COLOR,
            Color(0, 220, 50, 47),
            GRID_COLOR,
            Color(0, 220, 50, 47)]
        for color in colors:
            self._draw_frame()
            self._draw_hold(color)
            self._draw_queue()
            self._draw_grid()
            self._window.refresh()
            time.sleep(sleep_time)

    def _animate_line_clear(self, lines):
        w, h = self._game_view.grid.measures
        sleep_time = self._line_clear_speed / 4
        colors = [
            GRID_COLOR,
            LINE_CLEAR_COLOR,
            GRID_COLOR,
            LINE_CLEAR_COLOR]
        for i in range(4):
            for y in lines:
                SDL_FillRect(
                    self._surface,
                    SDL_Rect(
                        GRID_X_OFFSET * SQUARE_SIZE,
                        (GRID_Y_OFFSET + y) * SQUARE_SIZE,
                        w * SQUARE_SIZE,
                        SQUARE_SIZE),
                    colors[i])
            self._window.refresh()
            time.sleep(sleep_time)

    def render(self, request):
        type, arguments = request
        if type == RenderRequest.full:
            self._full_render()
        elif type == RenderRequest.line_clear:
            self._animate_line_clear(arguments)
        elif type == RenderRequest.cannot_hold:
            self._animate_cannot_hold(arguments)
