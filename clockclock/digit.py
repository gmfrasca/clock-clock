from clockclock.miniclock import MiniClock
from datetime import datetime


class Digit(object):

    def __init__(self, x, y, width, height, positions, canvas,
                 clockwise_only=True, rotate_on_same=True, snapping=3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = "X"
        self.positions = positions
        self.canvas = canvas

        self.clockwise_only = clockwise_only
        self.rotate_on_same = rotate_on_same
        self.snapping = snapping
        self.init_clockarray()

    def _get_position(self, value, x, y):
        now = datetime.now()
        default_h = int(datetime.strftime(now, "%M"))
        default_m = int(datetime.strftime(now, "%S"))
        try:
            position = self.positions.get(value)[y][x]
            h = position.get('hour', default_h)
            m = position.get('min', default_m)
            h = h if isinstance(h, int) else default_h
            m = m if isinstance(m, int) else default_m
            return h, m
        except Exception:
            return default_h, default_m

    def init_clockarray(self):
        self.clock_array = []
        for x in range(0, self.width):
            row = []
            for y in range(0, self.height):
                pos_h, pos_m = self._get_position(self.value, x, y)
                row.append(MiniClock(self.x + x, self.y + y, pos_h, pos_m, self.canvas))
            self.clock_array.append(row)

    def update(self, digit, next_digit, percent):
        percent = percent**self.snapping
        try:
            self.value = int(digit)
        except Exception:
            self.value = "any"
        try:
            self.nextval = int(next_digit)
        except Exception:
            self.nextval = "any"

        for x in range(0, self.width):
            for y in range(0, self.height):
                pos_h, pos_m = self._get_position(self.value, x, y)
                pos1_h, pos1_m = self._get_position(self.nextval, x, y)
                if self.clockwise_only:
                    if pos1_h < pos_h:
                        pos1_h += 12
                    if pos1_m < pos_m:
                        pos1_m += 60
                if self.rotate_on_same:
                    if pos1_h == pos_h:
                        pos1_h += 12
                    if pos1_m == pos_m:
                        pos1_m += 60
                h = (percent * (pos1_h - pos_h)) + pos_h
                m = (percent * (pos1_m - pos_m)) + pos_m
                self.clock_array[x][y].update_pos(h, m)
        self._draw()

    def _draw(self):
        for x in self.clock_array:
            for y in x:
                y.draw()
