import numpy as np
import cv2
from mss import mss

from screeninfo import get_monitors

class Screen:
    """ Deals with Screen issues """
    def __init__(self):
        self.p_mon = get_monitors()[0]
        w = 400
        h = 600
        self.sct = mss()

    def select_monitor(self, mon=0):
        """ Select the monitor to grab images from """
        self.p_mon = get_monitors()[mon]

    def select_box(self, top, left, width, height):
        """ Configures the box to read from """
        bounding_box = {'top': top-height-100, 'left': left - width, 'width': width, 'height': height}
        sct_img = self.sct.grab(bounding_box)
        return sct_img


# while True:

#     # TODO: Showing for debugging, not needed later
#     cv2.imshow('screen', np.array(sct_img))

#     if (cv2.waitKey(1) & 0xFF) == ord('q'):
#         cv2.destroyAllWindows()
#         break
