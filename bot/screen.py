""" @file screen.py
    @author Sean Duffie
    @brief Provides a tool for grabbing frames from the screen

    Allows the user to define the region of the screen to be observed, and to return a frame
    whenever prompted. The main interface involves a constructor to define the area, and a
    get_image() function to retrieve the current image at the time of the request. However there
    are additional features for dynamic resizing and changing monitors.

    TODO: In the future, this object could potentially be used to handle multiple video feeds
    simultaneously

    TODO: Add a "Box" class, which could allow more robust functionality for defining screen area
"""
import logging

import numpy as np
from mss import mss
from screeninfo import get_monitors

logger = logging.getLogger("Auto")


class Screen:
    """ Provides the ability to capture frames from the screen "
        TODO: Handle errors for out of bounds monitor
        TODO: Handle errors for improper screen bounds
    """
    def __init__(self, mon: int = 0, box = None):
        self.p_mon = get_monitors()[mon]

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
        """ Display a list of connected monitors and their specifications.

        Returns:
            list: list of Monitor objects from the screeninfo package.
        """
        mons = get_monitors()
        print(mons)
        return mons

    def change_monitor(self, mon, box = None):
        """ Select the monitor to grab images from

        Args:
            mon (int): index of selected monitor
            box (dict, optional): contains elements describing the desired section of the screen. Defaults to None.
        """
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
        """ Modify only the origin x-coordinate by a percentage of the monitor.

        See Screen.change_box() documentation for a description on how the box works

        Args:
            left (float): Ratio of the screen that left will start at.

        Returns:
            dict: a dictionary containing the new focus image dimensions
        """
        # TODO: if top+height > p_mon.height, then shrink the height
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
        """ Modify only the origin x-coordinate by a percentage of the monitor.

        See Screen.change_box() documentation for a description on how the box works

        Args:
            left (float): Ratio of the screen that left will start at.

        Returns:
            dict: a dictionary containing the new focus image dimensions
        """
        # TODO: if left+width > p_mon.width, then shrink the width
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
        """ Modify only the height of the image by a percentage of the monitor.

        See Screen.change_box() documentation for a description on how the box works

        Args:
            height (float): Percentage of the screen that the box-height will use.

        Returns:
            dict: a dictionary containing the new focus image dimensions
        """
        # TODO: if height+top > p_mon.height, then move the top up
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
        """ Modify only the width of the image by a percentage of the monitor.

        See Screen.change_box() documentation for a description on how the box works

        Args:
            width (float): Percentage of the screen that the box-width will use.

        Returns:
            dict: a dictionary containing the new focus image dimensions
        """
        # TODO: if width+left > p_mon.width, then move the left back
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
        """ Configures the box to read from.

        OpenCV images start coordinates from the top left corner, so the top of the image will
        have a lower y-coordinate than the bottom of the image. Likewise, the left of the image
        will have a lower x-coordinate than the right. Some of these functions will 

        Args:
            top (int): Y-coordinate for the pixel origin (top-left corner).
            left (int): X-coordinate for the pixel origin (top-left corner).
            width (int): How wide is the image.
            height (int): How tall is the image.

        Returns:
            dict: a dictionary containing the new focus image dimensions
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
