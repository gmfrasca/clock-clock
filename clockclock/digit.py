from clockclock.miniclock import MiniClock
from datetime import datetime


DEFAULT_H = 8
DEFAULT_M = 38


class Digit(object):

    def __init__(self, x, y, width, height, init_value, positions):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = init_value
        self.positions = positions
        self.init_clockarray()


    def _get_position(self, x, y):
        try:
            position = self.positions.get(self.value)[y][x]
            h = position.get('hour', DEFAULT_H)
            m = position.get('min', DEFAULT_M)
            h = h if isinstance(h, int) else DEFAULT_H
            m = m if isinstance(m, int) else DEFAULT_M
            return h, m
        except Exception as e:
            now = datetime.now()
            return (int(datetime.strftime(now, "%M")),
                    int(datetime.strftime(now, "%S")))

    def init_clockarray(self):
        self.clock_array = []
        for x in range(0, self.width):
            row = []
            for y in range(0, self.height):
                pos_h, pos_m = self._get_position(x, y)
                row.append(MiniClock(self.x + x, self.y + y, pos_h, pos_m))
            self.clock_array.append(row)

    def update(self, digit, canvas):
        try:
            self.value = int(digit)
        except Exception:
            self.value = "X"
        for x in range(0, self.width):
            for y in range(0, self.height):
                pos_h, pos_m = self._get_position(x, y)
                self.clock_array[x][y].update_pos(pos_h, pos_m)
        self._draw(canvas)

    def _draw(self, canvas):
        for x in self.clock_array:
            for y in x:
                y.draw(canvas)
