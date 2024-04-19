""" screen.py
    Provides a tool for grabbing frames from the screen
"""
import logging

import numpy as np
from mss import mss
from screeninfo import get_monitors

logger = logging.getLogger("Main.Screen")


class Screen:
    """ Provides the ability to capture frames from the screen "
        TODO: Handle errors for out of bounds monitor
        TODO: Handle errors for improper screen bounds
    """
    def __init__(self, mon: int = 0, box = None):
        self.p_mon = get_monitors()[mon]

        # TODO: Depricated, remove soon
        # self.width = int(self.p_mon.width/8)
        # self.height = int(self.p_mon.height/4)
        # self.top = self.p_mon.height - self.height - 100
        # self.left = self.p_mon.width - self.width
        if box is None:
            self.top = 0
            self.left = 0
            self.width = int(self.p_mon.width)
            self.height = int(self.p_mon.height)
        else:
            self.top = int(float(box["top"])*self.p_mon.height)
            self.left = int(float(box["left"])*self.p_mon.width)
            self.width = int(float(box["width"])*self.p_mon.width)
            self.height = int(float(box["height"])*self.p_mon.height)

        self.sct = mss()

        self.bounding_box = {
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height
        }
        # print(f"Bounding Box = {self.bounding_box}")

    def preview_monitors(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        mons = get_monitors()
        print(mons)
        return mons

    def change_monitor(self, mon, box = None):
        """ Select the monitor to grab images from """
        self.p_mon = get_monitors()[mon]

        # TODO: add default handling here for maintaining position/portions
        if box is None:
            self.width = int(self.p_mon.width/8)
            self.height = int(self.p_mon.height/4)
            self.top = self.p_mon.height - self.height - 100
            self.left = self.p_mon.width - self.width
        else:
            self.top = int(float(box["top"])*self.p_mon.height)
            self.left = int(float(box["left"])*self.p_mon.width)
            self.width = int(float(box["width"])*self.p_mon.width)
            self.height = int(float(box["height"])*self.p_mon.height)

        self.bounding_box = {
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height
        }
        # print(f"Bounding Box = {self.bounding_box}")

    def change_top(self, top: float):
        """_summary_

        Args:
            top (float): _description_
        """
        if top >= 0 and (self.p_mon.height*top)+self.height-1 < self.p_mon.height:
            self.top = int(self.p_mon.height*top)-1
            print(f"New Box Top = {self.top}")
        else:
            print("Invalid Top")

        self.bounding_box = {
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height
        }

        sct_img = self.sct.grab(self.bounding_box)
        return sct_img

    def change_left(self, left: float):
        """_summary_

        Args:
            left (float): _description_
        """
        if left >= 0 and (self.p_mon.width*left)+self.width-1 < self.p_mon.width:
            self.left = int(self.p_mon.width*left)-1
            print(f"New Box Left = {self.left}")
        else:
            print("Invalid Left")

        self.bounding_box = {
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height
        }

        sct_img = self.sct.grab(self.bounding_box)
        return sct_img

    def change_height(self, height: float):
        """_summary_

        Args:
            height (float): _description_
        """
        if height > 0 and self.top+(self.p_mon.height*height)-1 < self.p_mon.height:
            self.height = int(self.p_mon.height*height)-1
            print(f"New Box Height = {self.height}")
        else:
            print("Invalid Height")

        self.bounding_box = {
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height
        }

        sct_img = self.sct.grab(self.bounding_box)
        return sct_img

    def change_width(self, width: float):
        """_summary_

        Args:
            width (float): _description_
        """
        if width > 0 and self.left+(self.p_mon.width*width)-1 < self.p_mon.width:
            self.width = int(self.p_mon.width*width)-1
            print(f"New Box Width = {self.width}")
        else:
            print("Invalid Width")

        self.bounding_box = {
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height
        }

        sct_img = self.sct.grab(self.bounding_box)
        return sct_img

    def change_box(self, top: int, left: int, width: int, height: int):
        """ Configures the box to read from

        Args:
            top (int): _description_.
            left (int): _description_.
            width (int): _description_.
            height (int): _description_.

        Returns:
            _type_: _description_
        """

        self.top = top
        self.left = left
        self.width = width
        self.height = height

        self.bounding_box = {
            'top': top,
            'left': left,
            'width': width,
            'height': height
        }

        sct_img = self.sct.grab(self.bounding_box)
        return sct_img

    def get_image(self):
        """ Grabs the most recent screen frame """
        sct_img = np.array(self.sct.grab(self.bounding_box))
        return sct_img
