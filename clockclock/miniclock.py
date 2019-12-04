import math


MINICLOCK_RADIUS = 10


class MiniClock(object):

    def __init__(self, x, y, hour, minute):
        self.x = x
        self.y = y
        self.r = MINICLOCK_RADIUS
        self.x = self.r + 2 * self.r * x
        self.y = self.r + 2 * self.r * y
        self.hour = hour
        self.minute = minute

    def __repr__(self):
        return "{}:{}".format(self.hour, self.minute)

    def _get_hand_endpoint_coordinates(self, time, hourhand=True):
        r = self.r * .75 if hourhand else self.r
        time = time * 60 / 12 if hourhand else time
        time = 450 - (6 * time)  # minutes to degrees
        radians = math.radians(time)
        x = self.x + r * math.cos(radians)
        y = self.y - r * math.sin(radians)
        return x, y

    def update_pos(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def draw(self, canvas):
        hour_x, hour_y = self._get_hand_endpoint_coordinates(self.hour, hourhand=True)
        min_x, min_y = self._get_hand_endpoint_coordinates(self.minute, hourhand=False)

        canvas.create_oval(self.x-self.r, self.y-self.r,
                           self.x+self.r, self.y+self.r,
                           fill="white", width=2)
        canvas.create_line(self.x, self.y, hour_x, hour_y, width=2)
        canvas.create_line(self.x, self.y, min_x, min_y, width=2)
