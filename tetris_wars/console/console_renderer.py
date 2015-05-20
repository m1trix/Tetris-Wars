from engine.renderer import Renderer


class ConsoleRenderer(Renderer):

    def render(self):
        grid, tetrimino, ghost = self._render_unit.get_snapshot()
        w, h = grid.measures
        print("Engine measuers: {}".format((w, h)))
        for y in range(h):
            row = ''
            for x in range(w):
                if tetrimino.get_cell((x, y)):
                    symbol = '[]'
                elif ghost.get_cell((x, y)):
                    symbol = '::'
                elif grid.get_cell((x, y)):
                    symbol = '[]'
                else:
                    symbol = '  '
                row += symbol
            print('>|{}|<'.format(row))
        print(' +{}+'.format('--' * w))
        print('  {} '.format('/\\' * w))