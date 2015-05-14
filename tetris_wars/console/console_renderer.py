from engine.renderer import Renderer


class ConsoleRenderer(Renderer):

    def _render(self):
        w, h = self._engine.measures
        print("Engine measuers: {}".format((w, h)))
        for y in range(h):
            row = ''
            for x in range(w):
                b = self._engine.tetrimino
                b = b and self._engine.tetrimino.get_cell((x, y))

                b = b or self._engine.grid.get_cell((x, y))
                symbol = b and '[]' or '  '

                if not b and self._engine.ghost:
                    b = self._engine.ghost.get_cell((x, y))
                    symbol = b and '::' or '  '

                row += symbol
            print('>|{}|<'.format(row))
        print(' +{}+'.format('--' * w))
        print('  {} '.format('/\\' * w))

    def clear_lines(self, range):
        """ It will not be animated. """
        return None
