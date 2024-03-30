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

# for i in range(3):
#     logging.info("Starting in %d...", 3-i)
#     time.sleep(1)

last_time = datetime.datetime(2024, 3, 29, 10, 38, 00)
cur_time = datetime.datetime.now()
interval = datetime.timedelta(hours=2, minutes=0)
# interval = datetime.timedelta(minutes=1)
# interval = datetime.timedelta(seconds=5)
# keyboard.write("/bump\t")
# time.sleep(.5)
# keyboard.write("\n\n")

while True:
    while cur_time - last_time < interval:
        cur_time = datetime.datetime.now()
        remaining = interval - (cur_time - last_time)
        if (remaining.total_seconds()*10 // 10) % 60 == 0:
            logging.info("Time Remaining = %s", remaining)

        time.sleep(.1)

    logging.info("Writing to Keyboard")
    last_time = datetime.datetime.now()
    count = 3
    while count < 3:
        keyboard.write("/bump\t")
        time.sleep(.5)
        keyboard.write("\n\n")
        time.sleep(1)
        count += 1
