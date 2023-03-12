import numpy as np
import cv2
from mss import mss

from screeninfo import get_monitors
for m in get_monitors():
    print(str(m))

bounding_box = {'top': 800, 'left': 2160, 'width': 400, 'height': 600}

sct = mss()

while True:
    sct_img = sct.grab(bounding_box)
    cv2.imshow('screen', np.array(sct_img))

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
