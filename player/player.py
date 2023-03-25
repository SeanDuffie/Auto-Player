""" player.py

    This file handles any interactions that simulate the player.
    Right now it only deals with fishing, however more abilities
    could be added in the future.
"""
import time
import pyautogui as pg

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
