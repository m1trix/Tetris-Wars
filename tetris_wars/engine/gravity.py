from collections import deque
from engine.tetrimino import Segment
from engine.grid import Grid


class GravityCore:

    def __init__(self, grid):
        self._grid = grid
        w, h = grid.measures
        self._marked_segments = Grid(w, h)

    def regenerate_grid(self):
        w, h = self._grid.measures
        self._marked_segments = Grid(w, h)
        for y in range(h):
            for x in range(w):
                segment = self._grid.get_cell((x, y))
                if not segment or self._marked_segments.get_cell((x, y)):
                    continue
                new_segment = Segment(segment.get_type())
                for x, y in self._calculate_group(x, y, segment):
                    self._grid.set_cell((x, y), new_segment)
                    self._marked_segments.set_cell((x, y), True)

    def do_progress(self):
        w, h = self._grid.measures
        self._calculate_floating_segments()
        change = False
        for y in range(h - 2, -1, -1):
            for x in range(w):
                segment = self._grid.get_cell((x, y))
                if segment and self._can_segment_fall(x, y, segment):
                    change = True
                    self._grid.set_cell((x, y + 1), segment)
                    self._grid.set_cell((x, y), None)
        return change

    def _calculate_floating_segments(self):
        w, h = self._grid.measures
        self._marked_segments = Grid(w, h)
        for y in range(h):
            for x in range(w):
                segment = self._grid.get_cell((x, y))
                if not segment:
                    continue
                self._can_segment_fall(x, y, segment)

    def _can_segment_fall(self, x, y, segment):
        if self._marked_segments.get_cell((x, y)):
            return True
        w, h = self._grid.measures
        group = self._calculate_group(x, y, segment)
        return self._can_group_fall(group, segment)

    def _can_group_fall(self, group, segment):
        w, h = self._grid.measures
        for x, y in group:
            if y >= h - 1:
                return False
            under = self._grid.get_cell((x, y + 1))
            if not under or under is segment:
                continue
            if not self._can_segment_fall(x, y + 1, under):
                return False
        for x, y in group:
            self._marked_segments.set_cell((x, y), True)
        return True

    def _calculate_group(self, x, y, segment):
        w, h = self._grid.measures
        queue = deque([(x, y)])
        group = set()
        while queue:
            (x, y) = queue.popleft()
            if (x, y) in group:
                continue
            group.add((x, y))
            if x > 0 and self._grid.get_cell((x - 1, y)) == segment:
                queue.append((x - 1, y))
            if y > 0 and self._grid.get_cell((x, y - 1)) == segment:
                queue.append((x, y - 1))
            if x < w - 1 and self._grid.get_cell((x + 1, y)) == segment:
                queue.append((x + 1, y))
            if y < h - 1 and self._grid.get_cell((x, y + 1)) == segment:
                queue.append((x, y + 1))
        return group
