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

interval = datetime.timedelta(days=0, hours=4, minutes=0, seconds=0)
cur_time = datetime.datetime.now()
last_time = datetime.datetime(2024, 12, 26, 6, 0, 0)
# last_time = datetime.datetime.now() - datetime.timedelta(hours=11, minutes=59, seconds=55)
# interval = datetime.timedelta(minutes=2)
# interval = datetime.timedelta(seconds=5)

tags = ["@username"]
message = " message"

while True:
    cur_time = datetime.datetime.now()
    elapsed: datetime.timedelta = cur_time - last_time
    remaining: datetime.timedelta = interval - elapsed

    if (remaining.total_seconds()*10 // 10) % 3600 == 0:
        logging.info("Time Remaining = %s", remaining)

    if remaining.total_seconds() <= 0:
        logging.info("Writing to Keyboard")
        last_time = datetime.datetime.now()
        count = 0
        while count < 1:
            for tag in tags:
                # Write tags
                keyboard.write(tag)
                time.sleep(.5)
                keyboard.write("\t")
                # Write actual message
                keyboard.write(message)
                time.sleep(.5)
                keyboard.write("\n\n")
                time.sleep(1)

            # Send gif to test
            keyboard.write("https://tenor.com/view/sweet-victory-spongebob-sweet-sweet-victory-superbowl-gif-13419935")
            keyboard.write("\n\n")
            time.sleep(1)
            count += 1

    time.sleep(1)
