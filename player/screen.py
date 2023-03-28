""" screen.py
    Provides a tool for grabbing frames from the screen
"""
import numpy as np
from mss import mss

from screeninfo import get_monitors

class Screen:
    """ Provides the ability to capture frames from the screen """
    def __init__(self, mon=0):
        self.p_mon = get_monitors()[mon]
        self.width = int(self.p_mon.width/8)
        self.height = int(self.p_mon.height/4)
        self.box_top = self.p_mon.height - self.height - 100
        self.box_left = self.p_mon.width - self.width
        self.sct = mss()

        self.bounding_box = {
            'top': self.box_top,
            'left': self.box_left,
            'width': self.width,
            'height': self.height
        }



    def change_monitor(self, mon):
        """ Select the monitor to grab images from """
        self.p_mon = get_monitors()[mon]
        self.width = int(self.p_mon.width/8)
        self.height = int(self.p_mon.height/4)
        self.box_top = self.p_mon.height - self.height - 100
        self.box_left = self.p_mon.width - self.width

    def change_box(self, top, left, width, height):
        """ Configures the box to read from """
        bounding_box = {
            'top': top,
            'left': left,
            'width': width,
            'height': height
        }

        sct_img = self.sct.grab(bounding_box)
        return sct_img

    def get_image(self):
        """ Grabs the most recent screen frame """
        sct_img = np.array(self.sct.grab(self.bounding_box))
        return sct_img
