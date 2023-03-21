import keyboard
import pyautogui as pg
import time

def basic_fisher():
    """ Simple iteration of the auto fisher
        Does initial cast, then waits 10 seconds to recast
    """
    init_cast()

    while True:
        time.sleep(10)
        recast_fisher()

def init_cast():
    """ Initial cast of the rod """
    pg.rightClick()

def recast_fisher():
    """ Reels in and recasts """
    pg.rightClick()
    time.sleep(.1)
    pg.rightClick()

if __name__ == "__main__":
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

    basic_fisher()
