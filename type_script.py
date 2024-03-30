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

last_time = datetime.datetime(2024, 3, 29, 22, 38, 00)
cur_time = datetime.datetime.now()
interval = datetime.timedelta(hours=2, minutes=0)
# interval = datetime.timedelta(minutes=2)
# interval = datetime.timedelta(seconds=5)

while True:
    cur_time = datetime.datetime.now()
    elapsed: datetime.timedelta = cur_time - last_time
    remaining: datetime.timedelta = interval - elapsed

    if (remaining.total_seconds()*10 // 10) % 60 == 0:
        logging.info("Time Remaining = %s", remaining)

    if remaining.total_seconds() <= 0:
        logging.info("Writing to Keyboard")
        last_time = datetime.datetime.now()
        count = 0
        while count < 3:
            keyboard.write("/bump\t")
            time.sleep(.5)
            keyboard.write("\n\n")
            time.sleep(1)
            count += 1

    time.sleep(1)
