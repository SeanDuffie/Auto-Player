""" main.py
"""
import logging
import sys
import time

import cv2
import keyboard
from reader import ImgHandler
from screen import Screen

from player import Player

DEBUG = True

def minecraft():
    """ Reads audio subtitles and automatically casts/retrieves when fish grab the line

        Potential Phrases
            - Fishing Bobber Splashes
            - Fishing Bobber Thrown
            - Fishing Bobber Retrieved

            NOTE: Only individual words should be searched for, as Tesseract-OCR has a hard time
            reading the Minecraft font and often has typos.
    """
    # Initialize the Screen Capture and the Text Reader
    bbox = {
        "top": 0.75,
        "left": 0.84,
        "width": 0.16,
        "height": 0.16
    }
    scn = Screen(box=bbox)
    rdr = ImgHandler(scn.get_image())
    plyr = Player()

    # Give the user time to switch windows and then cast the rod
    logging.info("%s\t| Starting in\t3...", __name__)
    time.sleep(1)
    logging.info("%s\t| \t\t2...", __name__)
    time.sleep(1)
    logging.info("%s\t| \t\t1...", __name__)
    time.sleep(1)

    # Initial Click
    plyr.mouse_clicks(button="right")

    while True:
        # Grab a new image from the screen and read the text
        rdr.update_img(scn.get_image())
        try:
            text = rdr.read_text()
        except:
            logging.error("Failed to read Text")

        # If in debug mode, show the image being read, and the text that came from it
        if DEBUG:
            rdr.show_img()
            # logging.debug("%s\t| %s", __name__, text)

        # Parse text string from image
        if "Fishing" in text:       # Detect if the Bobber has a fish
            ltext: str = text.lower()

            # List of potential words that indicate the bobber has already been interacted with
            spam_words = ["thrown", "retr"]
            if not any(x in ltext for x in spam_words):  # Avoid spamming the reel after catch
                plyr.mouse_clicks(button="right", count=2, interval=0.25)

        # Quit out of the program if "q" or "esc" are pressed
        # FIXME: This is bad, it only registers if the focus is on an image preview
        Key = cv2.waitKeyEx(17)
        if Key in (27, 113):
            break
        if Key != -1:
            logging.info(Key)

def sevendays():
    """ Monitors Stamina and chooses to sprint or walk bases on exhaustion
    
        Control Logic
        - Reads "current/total stamina" (ex. "87/100")
        - if current stamina is greater than 90% of total, start sprinting
        - if current stamina is less than 10% of total, stop sprinting
    """
    # Initialize the Screen Capture and the Text Reader
    bbox = {
            "top": 0.9,
            "left": 0.035,
            "width": 0.055,
            "height": 0.05
    }
    scn = Screen(box=bbox)
    rdr = ImgHandler(scn.get_image())
    plyr = Player()

    # Give the user time to switch windows and then cast the rod
    logging.info("%s\t| Starting in\t3...", __name__)
    time.sleep(1)
    logging.info("%s\t| \t\t2...", __name__)
    time.sleep(1)
    logging.info("%s\t| \t\t1...", __name__)
    time.sleep(1)

    active: bool = False
    plyr.key_down("w")

    while True:
        # Grab a new image from the screen and read the text
        rdr.update_img(scn.get_image())
        # If in debug mode, show the image being read, and the text that came from it
        if DEBUG:
            rdr.show_img()

        # try:
        text: str = rdr.read_text()
        # except:
        #     logging.error("Failed to read Text")

        # Split values and remove incorrect numbers
        try:
            if text != "":
                # logging.info("%s\t| \t\t%s", __name__, text)
                current, total = text.split("/", 1)
                current = int("".join(c for c in current if c.isdigit()))
                total = int("".join(c for c in total if c.isdigit()))
                ratio = current/total
                logging.info("Ratio = %.2f", ratio)

                # if current is greater than 90% total, start sprinting
                if not active and ratio > .9:
                    plyr.key_down("w")
                    plyr.key_down("shiftleft")
                    active = True
                elif active and ratio < .1:
                    plyr.key_down("w")
                    plyr.key_up("shiftleft")
                    active = False
            else:
                logging.warning("No text detected")
        except ValueError:
            logging.error("Failed to split text")

        # Quit out of the program if "q" or "esc" are pressed
        # FIXME: This is bad, it only registers if the focus is on an image preview
        Key = cv2.waitKeyEx(17)
        if Key in (27, 113):
            plyr.key_up("w")
            plyr.key_up("shiftleft")
            break
        elif Key != -1:
            logging.info(Key)

def resize():
    """ Give user a chance to preview the readable screen area

        Resize the box by typing new percentages into the terminal
    """
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

    print("  1) Top\n  2) Left\n  3) Height\n  4) Width\n")

    while True:
        # Grab a new image from the screen and read the text
        rdr.update_img(scn.get_image())

        # If in debug mode, show the image being read, and the text that came from it
        if DEBUG:
            rdr.show_img()
        Key = cv2.waitKeyEx(17)
        match Key:
            case 49:
                new_top = float(input("Enter new top pixel (0-1, percent of screen): "))
                scn.change_top(new_top)
            case 50:
                new_left = float(input("Enter new left pixel (0-1, percent of screen): "))
                scn.change_left(new_left)
            case 51:
                new_height = float(input("Enter new image height (0-1, percent of screen): "))
                scn.change_height(new_height)
            case 52:
                new_width = float(input("Enter new image width (0-1, percent of screen): "))
                scn.change_width(new_width)
            case 27:
                break
            case 113:
                break
            case -1:
                pass
            case _:
                print(Key)

def main():
    """ Main function - will be run if this file is specified in terminal

        Launches the AutoFisher
    """
    # Initial Logger Settings
    fmt_main = "%(asctime)s\t| %(levelname)s\t| %(message)s"
    logging.basicConfig(format=fmt_main, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

    # TODO: Select Mode
    mode = int(input(
        "Enter the mode:\n 1) Minecraft Autofishing\n 2) 7 Days Autorunning\n 3) Resize\n"
    ))

    match mode:
        case 1:
            logging.info("%s\t| Minecraft settings", __name__)
            minecraft()
        case 2:
            logging.info("%s\t| 7 Days settings", __name__)
            sevendays()
        case 3:
            logging.info("%s\t| Custom settings", __name__)
            resize()
        case _:
            logging.info("%s\t| Unknown Mode", __name__)

        # Key = keyboard.read_key()
        # match Key:
        #     case -1:
        #         pass
        #     case _:
        #         logging.debug("%s\t| %d", __name__, Key)

if __name__ == "__main__":
    sys.exit(main())
