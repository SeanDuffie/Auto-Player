""" main.py
"""
import logging
import sys
import time

import cv2
import keyboard
from reader import ImgHandler
from screen import Screen

import player

DEBUG = True

def main():
    """ Main function - will be run if this file is specified in terminal

        Launches the AutoFisher
    """
    # Initial Logger Settings
    fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
    logging.basicConfig(format=fmt_main, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

    # Initialize the Screen Capture and the Text Reader
    scn = Screen()
    rdr = ImgHandler(scn.get_image())

    # Give the user time to switch windows and then cast the rod
    logging.info("%s\t| Starting in\t3...", __name__)
    time.sleep(1)
    logging.info("%s\t| \t\t2...", __name__)
    time.sleep(1)
    logging.info("%s\t| \t\t1...", __name__)
    time.sleep(1)
    player.init_cast()

    while True:
        # Grab a new image from the screen and read the text
        rdr.update_img(scn.get_image())
        text = rdr.read_text()

        # If in debug mode, show the image being read, and the text that came from it
        if DEBUG:
            rdr.show_img()
            logging.debug("%s\t| %s", __name__, text)

        """
        Potential Phrases
            - Fishing Bobber Splashes
            - Fishing Bobber Thrown
            - Fishing Bobber Retrieved

            NOTE: Only individual words should be searched for, as Tesseract-OCR has a hard time
            reading the Minecraft font and often has typos.
        """

        # Parse text string from image
        if "Fishing" in text:       # Detect if the Bobber has a fish

            # List of potential words that indicate the bobber has already been interacted with
            spam_words = ["Bobber", "Thrown", "Retrieved"]
            if spam_words not in text:  # Avoid spamming the reel until the first caption expires
                # Because recast_fisher() presses right click twice, it only needs to be called when 
                player.recast_fisher()

        # Quit out of the program if any key is pressed
        # FIXME: This is bad, it only registers if the focus is on an image preview
        Key = cv2.waitKey(17)
        # Key = keyboard.read_key()
        # if Key != -1:
        #     break

if __name__ == "__main__":
    sys.exit(main())
