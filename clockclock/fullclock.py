from clockclock.miniclock import MINICLOCK_RADIUS
from clockclock.digit import Digit
from datetime import datetime
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

    def __init__(self):
        # Setup Canvas
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,
                                width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT,
                                borderwidth=0,
                                highlightthickness=0,
                                bg="grey")
        # Setup Digits
        with open(POS_CONFIG) as f:
            self.positions = yaml.load(f, Loader=yaml.FullLoader)
        self.hour_tens = Digit(0, 0, DIGIT_WIDTH, DIGIT_HEIGHT, 1, self.positions,self.canvas)
        self.hour_ones = Digit(4, 0, DIGIT_WIDTH, DIGIT_HEIGHT, 2, self.positions, self.canvas)
        self.min_tens = Digit(8, 0, DIGIT_WIDTH, DIGIT_HEIGHT, 3, self.positions, self.canvas)
        self.min_ones = Digit(12, 0, DIGIT_WIDTH, DIGIT_HEIGHT, 4, self.positions, self.canvas)
        self.sec_tens = Digit(4, 6, DIGIT_WIDTH, DIGIT_HEIGHT, 1, self.positions, self.canvas)
        self.sec_ones = Digit(8, 6, DIGIT_WIDTH, DIGIT_HEIGHT, 2, self.positions, self.canvas)
        self.blank1 = Digit(0, 6, DIGIT_WIDTH, DIGIT_HEIGHT, "any", self.positions, self.canvas)
        self.blank2 = Digit(12, 6, DIGIT_WIDTH, DIGIT_HEIGHT, "any", self.positions, self.canvas)
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

    def draw(self):
        old_s = 0
        fps = 0

        while True:
            fps += 1
            now = datetime.now()
            h = datetime.strftime(now, "%H")
            m = datetime.strftime(now, "%M")
            s = datetime.strftime(now, "%S")
            if old_s != s:
                self.canvas.itemconfigure(self.fps_widget, text="FPS: {}".format(fps))
                fps = 0
            old_s = s
            self.hour_tens.update(h[0])
            self.hour_ones.update(h[1])
            self.min_tens.update(m[0])
            self.min_ones.update(m[1])
            self.sec_tens.update(s[0])
            self.sec_ones.update(s[1])
            self.blank1.update("any")
            self.blank2.update("any")
            self.canvas.update()
