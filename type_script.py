import time
import datetime
import keyboard
import winsound

for i in range(3):
    print(f"Starting in {3-i}...")
    winsound.PlaySound("*", winsound.SND_ALIAS)
    time.sleep(1)

last_time = datetime.datetime(2024, 3, 28, 18, 4)
cur_time = datetime.datetime.now()
keyboard.write("/bump\t")
# time.sleep(.5)
keyboard.write("\n\n")

while True:
    while cur_time - last_time < datetime.timedelta(hours=2):
        cur_time = datetime.datetime.now()
        remaining = datetime.timedelta(hours=2) - (cur_time - last_time)
        if remaining.total_seconds() < 7:
            winsound.PlaySound("*", winsound.SND_ALIAS)
        if (remaining.total_seconds() // 1) % 60 == 0:
            print(f"Time Remaining = {remaining}")

        time.sleep(1)

    keyboard.write("/bump\t")
    keyboard.write("\n\n")
    last_time = datetime.datetime.now()
