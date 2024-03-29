""" main.py
"""
import logging
# import multiprocessing as mp
import sys
import threading
import time

import cv2

import bot

DEBUG = True

# Initial Logger Settings
FMT_MAIN = "%(asctime)s\t| %(levelname)s\t| %(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")


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
    scn = bot.Screen(box=bbox)
    rdr = bot.ImgHandler(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()  # FIXME: Either make this optional or fix the lag
    t1 = threading.Thread(target=htky.run, args=())
    t1.start()

    # Initial Click
    plyr.mouse_clicks(button="right")

    while htky.alive:
        if htky.active:

            # Grab a new image from the screen and read the text
            rdr.update_img(scn.get_image())

            try:
                text = rdr.read_text()
            except UnboundLocalError: # Thrown when the image is blank or monocolor
                logging.error("Failed to read Text")
                text = ""

            # If in debug mode, show the image being read, and the text that came from it
            if DEBUG:
                rdr.show_img()
                logging.debug("%s\t| %s", __name__, text)

            # Parse text string from image
            if "Fishing" in text:       # Detect if the Bobber has a fish
                ltext: str = text.lower()

                # List of potential words that indicate the bobber has already been interacted with
                spam_words = ["thrown", "retr"]
                if not any(x in ltext for x in spam_words):  # Avoid spamming the reel after catch
                    plyr.mouse_clicks(button="right", count=2, interval=0.25)

        # Quit out of the program if "q" or "esc" are pressed
        else:
            logging.info("Inactive")
            while not htky.active:
                if htky.alive:
                    cv2.waitKey(17)
                else:
                    break
            logging.info("Active")

    t1.join()
    logging.info("End main")

def sevendays():
    """ Monitors Stamina and chooses to sprint or walk bases on exhaustion
    
        FIXME: Move threaded functions to hotkey.run()
        FIXME: Put keyboard.Listener on a Process rather than a thread
        FIXME: control() should be on the main thread
        FIXME: I might be able to get rid of the check() function by using htky.active directly
        
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
    scn = bot.Screen(box=bbox)
    rdr = bot.ImgHandler(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()  # FIXME: Either make this optional or fix the lag
    t1 = threading.Thread(target=htky.run, args=())
    t1.start()

    while htky.alive:
        if htky.active:
            plyr.key_down("w")

            # Grab a new image from the screen and read the text
            rdr.update_img(scn.get_image())

            # If in debug mode, show the image being read, and the text that came from it
            if DEBUG:
                rdr.show_img("Preview Raw")

            try:
                text: str = rdr.read_text()
            except UnboundLocalError: # Thrown when the image is blank or monocolor
                logging.error("Failed to read Text")
                text = ""

            # If in debug mode, show the image being read, and the text that came from it
            if DEBUG:
                rdr.show_img()

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
                    if ratio > .9:
                        plyr.key_down("shiftleft")
                    # if current is less than 10% total, stop sprinting
                    elif ratio < .1:
                        plyr.key_up("shiftleft")
                else:
                    logging.warning("No text detected")
                    # pass
            except ValueError:
                logging.error("Failed to split text")
                # pass
        else:
            logging.info("Inactive")
            plyr.key_up("w")
            plyr.key_up("shiftleft")
            while not htky.active:
                if htky.alive:
                    cv2.waitKey(17)
                else:
                    break
            logging.info("Active")

    t1.join()
    logging.info("End main")

def youtube():
    # Initialize the Screen Capture and the Text Reader
    bbox = {
        "top": 0.75,
        "left": 0.84,
        "width": 0.16,
        "height": 0.16
    }
    scn = bot.Screen(box=bbox)
    rdr = bot.ImgHandler(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()  # FIXME: Either make this optional or fix the lag
    t1 = threading.Thread(target=htky.run, args=())
    t1.start()

def aimer():
    # Initialize the Screen Capture and the Text Reader
    bbox = {
        "top": 0.75,
        "left": 0.84,
        "width": 0.16,
        "height": 0.16
    }
    scn = bot.Screen(box=bbox)
    rdr = bot.ImgHandler(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()  # FIXME: Either make this optional or fix the lag
    t1 = threading.Thread(target=htky.run, args=())
    t1.start()

def resize():
    """ Give user a chance to preview the readable screen area

        Resize the box by typing new percentages into the terminal
    """
    # Initialize the Screen Capture and the Text Reader
    scn = bot.Screen()
    rdr = bot.ImgHandler(scn.get_image())

    while True:
        # Grab a new image from the screen and read the text
        rdr.update_img(scn.get_image())
        # Show the image being read, and the text that came from it
        rdr.show_img()

        # Select the image with mouse, then use key inputs to modify
        logging.info('  1) Top    2) Left\n  3) Height\n  4) Width\r')
        Key = f"{input('Selected: ')}"
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
    """ Main function
        - Configures the logging features
        - Allows user to select game/mode
        - Launches the chosen automated feature
    """

    # Select Mode using the terminal
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
            logging.info("%s\t| YouTube settings", __name__)
            youtube()
        case 4:
            logging.info("%s\t| Aimlabs settings", __name__)
            aimer()
        case 5:
            logging.info("%s\t| Custom settings", __name__)
            resize()
        case _:
            logging.info("%s\t| Unknown Mode", __name__)

if __name__ == "__main__":
    sys.exit(main())
