""" @file main.py
    @author Sean Duffie
    @brief main runner for the Auto-Player program.
"""
import logging
import sys
import threading

import cv2

import bot
import logFormat

DEBUG = True

# Initial Logger Settings
logFormat.format_logs(logger_name="Auto")
logger = logging.getLogger("Auto")


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
        "left": 0.75,
        "width": 0.25,
        "height": 0.16
    }
    scn = bot.Screen(box=bbox)
    rdr = bot.Reader(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()
    t1 = threading.Thread(target=htky.run, args=())
    t1.start()

    while not htky.active:
        cv2.waitKey(17)

    # Initial Click
    plyr.mouse_clicks(button="right")

    while htky.alive:
        if htky.active:

            # Grab a new image from the screen and read the text
            rdr.update_img(scn.get_image())

            try:
                text = rdr.read_text()
            except UnboundLocalError: # Thrown when the image is blank or monocolor
                logger.error("Failed to read Text")
                text = ""

            # If in debug mode, show the image being read, and the text that came from it
            if DEBUG:
                rdr.show_img()
                logger.debug(text)

            # Parse text string from image
            if "Fishing" in text:       # Detect if the Bobber has a fish
                ltext: str = text.lower()

                # List of potential words that indicate the bobber has already been interacted with
                spam_words = ["thrown", "retr"]
                if not any(x in ltext for x in spam_words):  # Avoid spamming the reel after catch
                    plyr.mouse_clicks(button="right", count=2, interval=0.25)
                    # NOTE: This sleep is necessary so that there arent repeat recasts from the same sound
                    cv2.waitKey(3000)

        else:
            logger.info("Inactive")
            while not htky.active:
                if htky.alive:
                    cv2.waitKey(17)
                else:
                    break
            logger.info("Active")

    t1.join()
    logger.info("End main")

def sevendays():
    """ Monitors Stamina and chooses to sprint or walk bases on exhaustion

        FIXME: It would be cleaner to template the Hotkey interface

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
    rdr = bot.Reader(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()
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
                logger.error("Failed to read Text")
                text = ""

            # If in debug mode, show the image being read, and the text that came from it
            if DEBUG:
                rdr.show_img()

            # Split values and remove incorrect numbers
            try:
                if text != "":
                    logger.debug(text)
                    current, total = text.split("/", 1)
                    current = int("".join(c for c in current if c.isdigit()))
                    total = int("".join(c for c in total if c.isdigit()))
                    ratio = current/total
                    logger.info("Ratio = %.2f", ratio)

                    # if current is greater than 90% total, start sprinting
                    if ratio > .9:
                        plyr.key_down("shiftleft")
                    # if current is less than 10% total, stop sprinting
                    elif ratio < .1:
                        plyr.key_up("shiftleft")
                else:
                    logger.warning("No text detected")
                    # pass
            except ValueError:
                logger.error("Failed to split text")
                # pass
        else:
            logger.info("Inactive")
            plyr.key_up("w")
            plyr.key_up("shiftleft")
            while not htky.active:
                if htky.alive:
                    cv2.waitKey(17)
                else:
                    break
            logger.info("Active")

    t1.join()
    logger.info("End main")

def youtube():
    # Initialize the Screen Capture and the Text Reader
    bbox = {
        "top": 0.75,
        "left": 0.84,
        "width": 0.16,
        "height": 0.16
    }
    scn = bot.Screen(box=bbox)
    rdr = bot.Reader(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()
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
    rdr = bot.Reader(scn.get_image())
    plyr = bot.Player()
    htky = bot.Hotkey()
    t1 = threading.Thread(target=htky.run, args=())
    t1.start()

def resize():
    """ Give user a chance to preview the readable screen area

        Resize the box by typing new percentages into the terminal
    """
    # Initialize the Screen Capture and the Text Reader
    scn = bot.Screen()
    rdr = bot.Reader(scn.get_image())

    while True:
        # Grab a new image from the screen and read the text
        rdr.update_img(scn.get_image())
        # Show the image being read, and the text that came from it
        rdr.show_img()

        # Select the image with mouse, then use key inputs to modify
        logger.info('  1) Top    2) Left\n  3) Height\n  4) Width\r')
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
        "Enter the mode:\n 1) Minecraft Autofishing\n 2) 7 Days Autorunning\n 3) Youtube\n 4) Aimlabs\n 5) Resize\n"
    ))

    match mode:
        case 1:
            logger.info("Minecraft settings")
            minecraft()
        case 2:
            logger.info("7 Days settings")
            sevendays()
        case 3:
            logger.info("YouTube settings")
            youtube()
        case 4:
            logger.info("Aimlabs settings")
            aimer()
        case 5:
            logger.info("Custom settings")
            resize()
        case _:
            logger.info("Unknown Mode")


if __name__ == "__main__":
    sys.exit(main())
