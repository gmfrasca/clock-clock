from clockclock.miniclock import MINICLOCK_RADIUS
from clockclock.digit import Digit
from datetime import datetime, timedelta
from time import sleep

import tkinter as tk
import yaml
import os

POS_CONFIG = os.path.join(os.path.dirname(__file__), "..", "res", "positions.yaml")
DIGIT_WIDTH = 4
DIGIT_HEIGHT = 6
FPS_FONT = 15
CANVAS_WIDTH = 4 * DIGIT_WIDTH * 2 * MINICLOCK_RADIUS
CANVAS_HEIGHT = 2* DIGIT_HEIGHT * 2 * MINICLOCK_RADIUS + (1.5 * FPS_FONT)



class FullClock(object):

    def __init__(self, clockwise_only=True, rotate_on_same=True, snapping=3,
                 update_time=1):
        # Setup Canvas
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,
                                width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT,
                                borderwidth=0,
                                highlightthickness=0,
                                bg="grey")

        # Setup Digits
        self.update_time = update_time
        with open(POS_CONFIG) as f:
            self.positions = yaml.load(f, Loader=yaml.FullLoader)
        common_digit_args = {
            "width": DIGIT_WIDTH,
            "height": DIGIT_HEIGHT,
            "positions": self.positions,
            "canvas": self.canvas,
            "clockwise_only": clockwise_only,
            "rotate_on_same": rotate_on_same,
            "snapping": snapping
        }
        self.hour_tens = Digit(0, 0, **common_digit_args)
        self.hour_ones = Digit(4, 0, **common_digit_args)
        self.min_tens = Digit(8, 0,  **common_digit_args)
        self.min_ones = Digit(12, 0, **common_digit_args)
        self.sec_tens = Digit(4, 6,  **common_digit_args)
        self.sec_ones = Digit(8, 6,  **common_digit_args)
        self.blank1 = Digit(0, 6, **common_digit_args)
        self.blank2 = Digit(12, 6,  **common_digit_args)
        self.fps_widget = self.canvas.create_text(50, CANVAS_HEIGHT - (.5 * FPS_FONT),
                                                  fill="limegreen",
                                                  font=("courier", FPS_FONT, "bold"),
                                                  text="FPS: XXX")


        self.canvas.pack()

    def __repr__(self):
        return "{}{}:{}{}".format(self.hour_tens.value,
                                  self.hour_ones.value,
                                  self.min_tens.value,
                                  self.min_ones.value)

    def run(self):
        self.root.after(0, self.draw)
        self.root.mainloop()

    def _update(self):
        now = datetime.now()
        if now > self.next:
            print("set")
            self.now = now
            self.next = now + timedelta(seconds=self.update_time)

        h = datetime.strftime(self.now, "%H")
        m = datetime.strftime(self.now, "%M")
        s = datetime.strftime(self.now, "%S")

        h1 = datetime.strftime(self.next, "%H")
        m1 = datetime.strftime(self.next, "%M")
        s1 = datetime.strftime(self.next, "%S")

        timediff = (self.next - now)
        percent = (self.update_time - timediff.seconds - timediff.microseconds/1000000 ) / self.update_time

        self.hour_tens.update(h[0], h1[0], percent)
        self.hour_ones.update(h[1], h1[1], percent)
        self.min_tens.update(m[0], m1[0], percent)
        self.min_ones.update(m[1], m1[1], percent)
        self.sec_tens.update(s[0], s1[0], percent)
        self.sec_ones.update(s[1], s1[1], percent)
        self.blank1.update("any", "any", percent)
        self.blank2.update("any", "any", percent)
        self.canvas.update()

    def draw(self):
        old_s = 0
        fps = 0
        self.next = datetime.now()
        self.now = datetime.now()

        try:
            # Wait until an even time
            while datetime.now().second % self.update_time != 0:
                sleep(.1)
            while True:
                fps += 1
                now = datetime.now()
                s = datetime.strftime(now, "%S")
                if old_s != s:
                    self.canvas.itemconfigure(self.fps_widget, text="FPS: {}".format(fps))
                    fps = 0
                old_s = s
                self._update()
        except tk.TclError as tke:
            pass
