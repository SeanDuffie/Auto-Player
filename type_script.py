""" @file type_script.py
    @author Sean Duffie
    @brief Made purely to spite Ratoz
"""
import datetime
import logging
import time

import keyboard

# Initial Logger Settings
FMT_MAIN = "%(asctime)s\t| %(levelname)s\t| %(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

for i in range(3):
    logging.info("Starting in %d...", 3-i)
    time.sleep(1)

last_time = datetime.datetime(2024, 3, 28, 18, 4)
cur_time = datetime.datetime.now()
keyboard.write("/bump\t")
time.sleep(.5)
keyboard.write("\n\n")

while True:
    while cur_time - last_time < datetime.timedelta(hours=2):
        cur_time = datetime.datetime.now()
        remaining = datetime.timedelta(hours=2) - (cur_time - last_time)
        if (remaining.total_seconds() // 1) % 60 == 0:
            logging.info("Time Remaining = %s", remaining)

        time.sleep(1)

    keyboard.write("/bump\t")
    time.sleep(.5)
    keyboard.write("\n\n")
    last_time = datetime.datetime.now()
